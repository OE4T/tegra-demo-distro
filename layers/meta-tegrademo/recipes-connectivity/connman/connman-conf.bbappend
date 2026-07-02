FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI:append:tegra264 = " file://main.conf.tegra264"

do_install:append:tegra264() {
    install -d ${D}${sysconfdir}/connman
    install -m 0644 ${UNPACKDIR}/main.conf.tegra264 ${D}${sysconfdir}/connman/main.conf
}
