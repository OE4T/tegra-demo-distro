SUMMARY = "First-boot /data partition creation, mount, and overlayfs setup"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

inherit systemd overlayfs

DATA_PARTITION_OVERLAY_WRITABLE_PATHS ?= "/etc/ssh /etc/NetworkManager/system-connections"
OVERLAYFS_WRITABLE_PATHS[data] = "${DATA_PARTITION_OVERLAY_WRITABLE_PATHS}"

SRC_URI = " \
    file://10-data-overlays.conf \
    file://50-data.conf \
    file://data.mount \
"

S = "${UNPACKDIR}"

RDEPENDS:${PN} = "systemd"

SYSTEMD_SERVICE:${PN} = "data.mount"
SYSTEMD_AUTO_ENABLE:${PN} = "enable"

FILES:${PN} += " \
    ${nonarch_libdir}/repart.d/ \
    ${systemd_system_unitdir}/sshdgenkeys.service.d/ \
    ${systemd_system_unitdir}/NetworkManager.service.d/ \
    /data \
"

do_install() {
    install -d ${D}${nonarch_libdir}/repart.d
    install -m 0644 ${S}/50-data.conf ${D}${nonarch_libdir}/repart.d/

    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${S}/data.mount ${D}${systemd_system_unitdir}/

    install -d ${D}${systemd_system_unitdir}/sshdgenkeys.service.d
    install -m 0644 ${S}/10-data-overlays.conf \
        ${D}${systemd_system_unitdir}/sshdgenkeys.service.d/

    install -d ${D}${systemd_system_unitdir}/NetworkManager.service.d
    install -m 0644 ${S}/10-data-overlays.conf \
        ${D}${systemd_system_unitdir}/NetworkManager.service.d/

    install -d ${D}/data
}
