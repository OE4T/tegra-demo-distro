DESCRIPTION = "Script run as a part of swupdate install for tegra"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER ??= ""

SRC_URI = "\
    file://tegra-swupdate-script.lua.in \
"

inherit deploy

require tegra-swupdate.inc

do_compile() {
    unpackdir=${WORKDIR}
    if [ -n "${UNPACKDIR}" -a -d "${UNPACKDIR}" ]; then
        echo "Hack for supporting kirkstone->styhead through https://github.com/yoctoproject/poky/commit/d24a7d0fb16457e10e7a216d4c9ae3fb265113d1"
        echo "For styhead and later branches you can delete this logic and replace with UNPACKDIR"
        unpackdir=${UNPACKDIR}
    fi
    sed -e's,@TEGRA_SWUPDATE_BOOTLOADER_INSTALL_ONLY_IF_DIFFERENT@,${TEGRA_SWUPDATE_BOOTLOADER_INSTALL_ONLY_IF_DIFFERENT},g' \
        -e's,@TEGRA_SWUPDATE_CAPSULE_INSTALL_PATH@,${TEGRA_SWUPDATE_CAPSULE_INSTALL_PATH},g'\
        -e's,@TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER@,${TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER},g'\
        ${unpackdir}/tegra-swupdate-script.lua.in > ${B}/tegra-swupdate-script.lua
}

do_deploy() {
    cp ${B}/tegra-swupdate-script.lua ${DEPLOYDIR}/
}

addtask deploy after do_install
