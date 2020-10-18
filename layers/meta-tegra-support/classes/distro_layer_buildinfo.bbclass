def dlb_git_describe(path):
    if path is not None:
        with os.popen("cd %s; git describe --dirty --always 2>/dev/null" % path) as f:
            gitinfo = f.read().strip()
        return gitinfo
    return ""

def dlb_git_branch(path):
    branchname = ""
    if path is not None:
        with os.popen("cd %s; git branch 2>/dev/null" % path) as f:
            for line in f:
                if line.startswith("* "):
                    branchname = line[2:].strip()
                    break
    return branchname

def distro_layername(d):
    return d.getVar("DISTRO_LAYER", True)

def distro_layerpath(lname, d):
    layers = {os.path.basename(l): l for l in (d.getVar("BBLAYERS", True) or "").split()}
    try:
        return layers[lname]
    except KeyError:
        return None

def distro_layer_buildtag(d):
    tag = dlb_git_describe(distro_layerpath(distro_layername(d), d))
    if os.getenv("USER") in ['jenkins', 'builder'] or bb.utils.to_boolean(d.getVar("PRODUCTION_BUILD")):
        return '-' + tag
    return '-' + tag + '-' + os.getenv("USER")

def distro_layer_branch(d):
    return dlb_git_branch(distro_layerpath(distro_layername(d), d))

DISTRO_LAYER ??= "meta-${DISTRO}"
DISTRO_LAYER_BUILDTAG := "${@distro_layer_buildtag(d)}"
DISTRO_LAYER_BUILDTAG[vardepvalue] = "${DISTRO_LAYER_BUILDTAG}"
DISTRO_LAYER_BRANCH := "${@distro_layer_branch(d)}"
DISTRO_LAYER_BRANCH[vardepvalue] = "${DISTRO_LAYER_BRANCH}"
