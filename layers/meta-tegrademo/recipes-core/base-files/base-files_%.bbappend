FILESEXTRAPATHS_prepend := "${THISDIR}/${BPN}:"

SRC_URI_append_tegrademo-mender_jetson-nano-2gb-devkit = " file://fstab-swap"

dirs755_append_tegrademo-mender = " /data"

do_install_append_tegrademo-mender_jetson-nano-2gb-devkit() {
    cat ${WORKDIR}/fstab-swap >>${D}${sysconfdir}/fstab
}

RDEPENDS_${PN}_append_tegrademo-mender = " data-overlay-setup"
RDEPENDS_${PN}_append_tegrademo-mender_jetson-nano-2gb-devkit = " util-linux-mkswap util-linux-swaponoff"
RRECOMMENDS_${PN}_append_tegrademo-mender = " kernel-module-overlay"
