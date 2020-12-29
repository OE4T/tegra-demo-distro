FILESEXTRAPATHS_prepend := "${THISDIR}/${BPN}:"

SRC_URI += "file://target-mkdir.conf"

do_install_append() {
    install -d ${D}${sysconfdir}/systemd/system/setup-nv-boot-control.service.d
    install -m 0644 ${WORKDIR}/target-mkdir.conf ${D}${sysconfdir}/systemd/system/setup-nv-boot-control.service.d/
}

FILES_${PN}-service += "${sysconfdir}/systemd/system/setup-nv-boot-control.service.d"
