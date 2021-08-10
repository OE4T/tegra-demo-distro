DESCRIPTION = "Script to set up directories for overlayfs mounts on /data"
HOMEPAGE = "https://github.com/OE4T"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"
DEPENDS = ""

SRC_URI = "\
    file://data-overlay-setup.sh.in \
    file://data-overlay-setup.service.in \
"

S = "${WORKDIR}"
B = "${WORKDIR}/build"

inherit systemd

do_compile() {
    for inf in ${S}/*.in; do
        [ -e $inf ] || continue
        outf=$(basename $inf .in)
        sed -e 's,@BINDIR@,${bindir},g' \
            -e 's,@SBINDIR@,${sbindir},g' \
            -e 's,@SYSCONFDIR@,${sysconfdir},g' \
	    -e 's,@BASE_BINDIR@,${base_bindir},g' \
	    -e 's,@BASE_SBINDIR@,${base_sbindir},g' \
	    -e 's,@NONARCH_BASE_LIBDIR@,${nonarch_base_libdir},g' \
	    $inf > ${B}/$outf
    done
}

do_install() {
    install -d ${D}${sbindir} ${D}${systemd_system_unitdir}
    install -m 0755 ${B}/data-overlay-setup.sh ${D}${sbindir}/data-overlay-setup
    install -m 0644 ${B}/data-overlay-setup.service ${D}${systemd_system_unitdir}/
}

SYSTEMD_SERVICE:${PN} = "data-overlay-setup.service"
