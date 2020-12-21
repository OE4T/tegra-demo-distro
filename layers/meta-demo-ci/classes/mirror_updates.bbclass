# Class for automatically populating downloads and/or sstate mirrors
# during builds, when the mirrors are separate from the normal, local
# DL_DIR and SSTATE_DIR used to perform the build.
#
# Supports file:// and s3:// URLs.
# S3 support also requires the lib/oeaws/s3session.py module.

# For updating the downloads mirror:
#  - set UPDATE_DOWNLOADS_MIRROR to "1" and
#  - set DOWNLOADS_MIRROR_URL to the URL for the mirror
# You should also set BB_GENERATE_MIRROR_TARBALLS to "1" so
# that tarballs of any SCM repositories get uploaded to the
# mirror.
UPDATE_DOWNLOADS_MIRROR ?= "0"
DOWNLOADS_MIRROR_URL ??= ""

# For updating the shared state mirror:
#  - set UPDATE_SSTATE_MIROR to "1" and
#  - set SSTATE_MIRROR_URL to the URL for the mirror
UPDATE_SSTATE_MIRROR ?= "0"
SSTATE_MIRROR_URL ??= ""

python downloads_mirror_update() {
    import os, shutil, urllib.parse

    src_uri = (d.getVar("SRC_URI") or "").split()
    if len(src_uri) == 0:
        return

    mirror = urllib.parse.urlparse(d.getVar("DOWNLOADS_MIRROR_URL"))

    s3 = None
    if mirror.scheme == 's3':
        from oeaws import s3session
        s3 = s3session.S3Session()
    elif mirror.scheme != 'file':
        bb.warn("unsupported DOWNLOADS_MIRROR_URL type: %s" % mirror.scheme)
        return
    fetcher = bb.fetch2.Fetch(src_uri, d)
    dl_dir = d.getVar("DL_DIR")
    for url in src_uri:
        # We don't mirror when the SRC_URI is a file://, since those
        # aren't actually downloaded
        if urllib.parse.urlparse(url).scheme == 'file':
            continue
        if hasattr(fetcher.ud[url], 'fullmirror'):
            localfile = fetcher.ud[url].fullmirror
        else:
            localfile = fetcher.localpath(url)
        # Only files get mirrored, not directories
        if not os.path.exists(localfile) or os.path.isdir(localfile):
            continue
        remotefile = localfile[len(dl_dir)+1:]
        if not s3:
            # When mirroring to the local filesystem, don't mirror symlinks
            if os.path.islink(localfile):
                continue
            mirrorfile = os.path.join(mirror.path, remotefile)
            bb.utils.mkdirhier(os.path.dirname(mirrorfile))
            lf = bb.utils.lockfile("%s.lock" % mirrorfile)
            try:
                bb.debug(1, "copying: %s -> %s" % (localfile, mirrorfile))
                shutil.copyfile(localfile, mirrorfile)
            except IOError:
                bb.warn("error copying %s to %s" % (localfile, mirrorfile))
            bb.utils.unlockfile(lf)
        else:
            mirrorpath = mirror.path.split('/')
            mirrorpath.append(remotefile)
            destobj = '/'.join(mirrorpath[1:])
            info = s3.get_object_info(mirror.netloc, destobj)
            if info and 'LastModified' in info:
                mtime = int(time.mktime(info['LastModified'].timetuple()))
                st = os.stat(localfile)
                if info['ContentLength'] == st.st_size and int(st.st_mtime) == mtime:
                    continue
            s3.upload(localfile, mirror.netloc, destobj)
}

python sstate_mirror_update() {
    import os, shutil, urllib.parse

    if d.getVar('SSTATE_SKIP_CREATION') == '1':
        return

    mirror = urllib.parse.urlparse(d.getVar("SSTATE_MIRROR_URL"))
    if mirror.scheme == 'file':
        sstatepkg = d.getVar("SSTATE_PKG")
        mirrorpkg = os.path.join(mirror.path, d.getVar("SSTATE_PKGNAME"))
        bb.utils.mkdirhier(os.path.dirname(mirrorpkg))
        lf = bb.utils.lockfile("%s.lock" % mirrorpkg)
        try:
            bb.debug(1, "copying: %s -> %s" % (sstatepkg, mirrorpkg))
            shutil.copyfile(sstatepkg, mirrorpkg)
            shutil.copyfile(sstatepkg + ".siginfo", mirrorpkg + ".siginfo")
        except IOError:
            bb.warn("error copying %s to %s" % (sstatepkg, mirrorpkg))
        bb.utils.unlockfile(lf)
    elif mirror.scheme == 's3':
        from oeaws import s3session

        mirrorpath = mirror.path.split('/')
        mirrorpath.append(d.getVar("SSTATE_PKGNAME"))
        sstatepkg = d.getVar("SSTATE_PKG")
        destobj = '/'.join(mirrorpath[1:])
        s3 = s3session.S3Session()
        s3.upload(sstatepkg, mirror.netloc, destobj)
        s3.upload(sstatepkg + ".siginfo", mirror.netloc, destobj + ".siginfo")
    else:
        bb.warn("unsupported SSTATE_MIRROR_URL type: %s" % mirror.scheme)
}


python () {
    import os, urllib.parse

    try:
        from oeaws import s3session
    except ImportError:
        pass

    if bb.utils.to_boolean(d.getVar("UPDATE_DOWNLOADS_MIRROR")):
        mirror = urllib.parse.urlparse(d.getVar("DOWNLOADS_MIRROR_URL"))
        enable = False
        if mirror.scheme == 'file':
            if os.access(mirror.path, os.W_OK):
                enable = True
            else:
                bb.warn("DOWNLOADS_MIRROR_URL (%s) not writable" % mirror.path)
        elif mirror.scheme == 's3':
            if s3session:
                enable = True
            else:
                bb.warn("UPDATE_DOWNLOADS_MIRROR enabled but s3session module cannot be loaded")
        else:
            bb.warn("UPDATE_DOWNLOADS_MIRROR enabled, but DOWNLOADS_MIRROR_URL not file:// or s3:// URL")

        if enable:
            postfuncs = (d.getVarFlag("do_fetch", "postfuncs") or "").split()
            if "downloads_mirror_update" not in postfuncs:
                d.appendVarFlag("do_fetch", "postfuncs", " downloads_mirror_update")
                d.appendVarFlag("do_fetch", "vardepsexclude", " downloads_mirror_update")

    if bb.utils.to_boolean(d.getVar("UPDATE_SSTATE_MIRROR")):
        enable = False
        mirror = urllib.parse.urlparse(d.getVar("SSTATE_MIRROR_URL"))
        if mirror.scheme == 'file':
            if os.access(mirror.path, os.W_OK):
                enable = True
            else:
                bb.warn("SSTATE_MIRROR_URL (%s) not writable, skipping updates" % mirror.path)
        elif mirror.scheme == 's3':
            if s3session:
                enable = True
            else:
                bb.warn("UPDATE_SSTATE_MIRROR enabled but s3session module cannot be loaded")
        else:
            bb.warn("UPDATE_SSTATE_MIRROR enabled, but SSTATE_MIRROR_URL not file:// or s3:// URL")

        if enable:
            for task in (d.getVar("SSTATETASKS") or "").split():
                postfuncs = (d.getVarFlag(task, "postfuncs") or "").split()
                if "sstate_task_postfunc" in postfuncs and "sstate_mirror_update" not in postfuncs:
                    d.appendVarFlag(task, "postfuncs", " sstate_mirror_update")
                    d.appendVarFlag(task, "vardepsexclude", " sstate_mirror_update")

}
