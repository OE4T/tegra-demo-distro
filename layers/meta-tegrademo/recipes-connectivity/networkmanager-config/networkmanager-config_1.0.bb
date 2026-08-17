SUMMARY = "NetworkManager configuration for Tegra platforms"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

COMPATIBLE_MACHINE = "(tegra264)"

SRC_URI = "file://70-tegra-mgbe-unmanaged.conf"

do_install() {
    install -d ${D}${sysconfdir}/NetworkManager/conf.d
    install -m 0644 ${UNPACKDIR}/70-tegra-mgbe-unmanaged.conf ${D}${sysconfdir}/NetworkManager/conf.d/
}

FILES:${PN} = "${sysconfdir}/NetworkManager/conf.d/70-tegra-mgbe-unmanaged.conf"

RDEPENDS:${PN} = "networkmanager"
