DESCRIPTION = "Machine-specific configuration for swupdate"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

require tegra-swupdate.inc

SRC_URI = "\
    file://swupdate.cfg.in \
    file://swupdate-genconfig.sh.in \
    file://swupdate-mods.conf.in \
"

SRC_URI:append:secureboot = " \
    file://swupdate.pem \
"

SWUPDATE_BOARDNAME ??= "${MACHINE}"
SWUPDATE_HWREVISION ??= "1.0"
TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER ??= ""

S = "${UNPACKDIR}"
B = "${WORKDIR}/build"

do_compile() {
    rm -f ${B}/hwrevision
    echo "${SWUPDATE_BOARDNAME} ${SWUPDATE_HWREVISION}" > ${B}/hwrevision
    sed -e's,@MODEL@,${SWUPDATE_BOARDNAME},g' \
	    ${S}/swupdate.cfg.in > ${B}/swupdate.cfg.in
    sed -e's,@DATADIR@,${datadir},g' \
        -e"s,@TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER@,${TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER},g" \
	    ${S}/swupdate-genconfig.sh.in > ${B}/swupdate-genconfig.sh
    echo "tegra-bootloader-capsule    ${TEGRA_SWUPDATE_BOOTLOADER_VERSION}" > ${B}/sw-versions-thisslot
    TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER_DIR_DEPENDS=""
    if [ -n "${TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER}" ]; then
        TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER_DIR_DEPENDS="WantsMountsFor=$(dirname ${TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER})"
    fi
    sed -e"s,@TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER_DIR_DEPENDS@,${TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER_DIR_DEPENDS},g" \
        ${S}/swupdate-mods.conf.in > ${B}/swupdate-mods.conf
}

do_install() {
    install -d ${D}${sysconfdir}
    install -m 0644 ${B}/hwrevision ${D}${sysconfdir}/
    ln -s /run/swupdate/swupdate.cfg ${D}${sysconfdir}/swupdate.cfg
    install -d ${D}${datadir}/swupdate
    install -m 0644 ${B}/swupdate.cfg.in ${D}${datadir}/swupdate/
    install -d ${D}${libexecdir}/swupdate
    install -m 0755 ${B}/swupdate-genconfig.sh ${D}${libexecdir}/swupdate/swupdate-genconfig
    install -d ${D}${sysconfdir}/systemd/system/swupdate.service.d
    install -m 0644 ${B}/swupdate-mods.conf ${D}${sysconfdir}/systemd/system/swupdate.service.d/
    install -m 0644 ${B}/sw-versions-thisslot ${D}${datadir}/swupdate/
    ln -s /run/swupdate/sw-versions ${D}${sysconfdir}/sw-versions
    if [ -n "${TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER}" ]; then
        installdir=$(dirname ${TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER})
        install -d ${D}$installdir
        touch ${D}${installdir}/$(basename ${TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER}0)
        touch ${D}${installdir}/$(basename ${TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER}1)
    fi
}

do_install:append:secureboot() {
    install -m 0644 ${S}/swupdate.pem ${D}${datadir}/swupdate/
}

FILES:${PN} += "${datadir}/swupdate"
FILES:${PN} += "${sysconfdir}/sw-versions"
FILES:${PN} += "/data/*"
PACKAGE_ARCH = "${MACHINE_ARCH}"
EXTRADEPS = "tegra-redundant-boot"
RDEPENDS:${PN} += "${EXTRADEPS}"
