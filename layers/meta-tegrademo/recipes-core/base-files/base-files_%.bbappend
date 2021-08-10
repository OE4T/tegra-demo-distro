FILESEXTRAPATHS:prepend := "${THISDIR}/${BPN}:"

SRC_URI:append:tegrademo-mender_jetson-nano-2gb-devkit = " file://fstab-swap"

dirs755:append:tegrademo-mender = " /data"

do_install:append:tegrademo-mender_jetson-nano-2gb-devkit() {
    cat ${WORKDIR}/fstab-swap >>${D}${sysconfdir}/fstab
}

RDEPENDS:${PN}:append:tegrademo-mender = " data-overlay-setup"
RDEPENDS:${PN}:append:tegrademo-mender_jetson-nano-2gb-devkit = " util-linux-mkswap util-linux-swaponoff"
RRECOMMENDS:${PN}:append:tegrademo-mender = " kernel-module-overlay"
