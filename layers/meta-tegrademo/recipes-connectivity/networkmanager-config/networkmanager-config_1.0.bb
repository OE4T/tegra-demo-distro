SUMMARY = "NetworkManager configuration for Tegra platforms"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

COMPATIBLE_MACHINE = "(tegra)"
PACKAGE_ARCH = "${SOC_FAMILY_PKGARCH}"

SRC_URI = "file://l4tbr0-online.conf"
SRC_URI:append:tegra264 = " file://70-tegra-mgbe-unmanaged.conf"

S = "${UNPACKDIR}"

do_install() {
    install -d ${D}${sysconfdir}/systemd/network/70-l4tbr0.network.d
    install -m 0644 ${UNPACKDIR}/l4tbr0-online.conf \
        ${D}${sysconfdir}/systemd/network/70-l4tbr0.network.d/50-tegrademo-online.conf
}

do_install:append:tegra264() {
    install -d ${D}${sysconfdir}/NetworkManager/conf.d
    install -m 0644 ${UNPACKDIR}/70-tegra-mgbe-unmanaged.conf ${D}${sysconfdir}/NetworkManager/conf.d/
}

FILES:${PN} = " \
    ${sysconfdir}/systemd/network/70-l4tbr0.network.d \
    ${sysconfdir}/NetworkManager/conf.d \
"

RDEPENDS:${PN} = "networkmanager"
