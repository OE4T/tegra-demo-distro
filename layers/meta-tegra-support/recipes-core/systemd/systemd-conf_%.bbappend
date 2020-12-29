FILESEXTRAPATHS_prepend := "${THISDIR}/${BPN}:"

SRC_URI += "file://skip-dummy-interfaces.conf"

do_install_append() {
    install -d ${D}${sysconfdir}/systemd/network/80-wired.network.d
    install -m 0644 ${WORKDIR}/skip-dummy-interfaces.conf ${D}${sysconfdir}/systemd/network/80-wired.network.d/
}

FILES_${PN} += "${sysconfdir}/systemd/network"
