DESCRIPTION = "Packagegroup for inclusion in all Tegra demo weston images"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS_${PN} = " \
    weston \
    weston-init \
    ${@bb.utils.contains('DISTRO_FEATURES', 'x11', 'weston-xwayland matchbox-terminal', '', d)} \
"
