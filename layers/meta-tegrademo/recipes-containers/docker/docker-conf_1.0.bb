DESCRIPTION = "Service configuration drop-in for docker"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "\
    file://docker-storage-redirect.conf \
    file://docker-overlay.fstab \
"

S = "${WORKDIR}"

do_install() {
    if [ -s ${S}/docker-storage-redirect.conf ]; then
        install -d ${D}${systemd_system_unitdir}/docker.service.d
        install -m 0644 ${S}/docker-storage-redirect.conf ${D}${systemd_system_unitdir}/docker.service.d/
    fi
    if [ -s ${S}/docker-overlay.fstab ]; then
        install -d ${D}${sysconfdir}
        install -m 0644 ${S}/docker-overlay.fstab ${D}${sysconfdir}/
    fi
}

pkg_postinst:${PN}() {
    if [ -e $D${sysconfdir}/docker-overlay.fstab ]; then
        cat $D${sysconfdir}/docker-overlay.fstab >> $D${sysconfdir}/fstab
        rm -f $D${sysconfdir}/docker-overlay.fstab
    fi
}
ALLOW_EMPTY:${PN} = "1"
FILES:${PN} = "${systemd_system_unitdir} ${sysconfdir}"
RDEPENDS:${PN} = "base-files"
PACKAGE_ARCH = "${MACHINE_ARCH}"

