DESCRIPTION = "Packagegroup for inclusion in all Tegra demo weston images"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS_${PN} = " \
    clutter-1.0-examples \
    gtk+3-demo \
    wayland-utils \
    weston \
    weston-examples \
    weston-init \
    ${@bb.utils.contains('DISTRO_FEATURES', 'x11', 'weston-xwayland matchbox-terminal', '', d)} \
"
