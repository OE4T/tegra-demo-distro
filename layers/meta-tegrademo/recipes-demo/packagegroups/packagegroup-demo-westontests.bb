DESCRIPTION = "Packagegroup for Tegra demo weston test applications"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    ${@bb.utils.contains('DISTRO_FEATURES', 'x11', 'gstreamer-tests', '', d)} \
    l4t-graphics-demos-wayland \
    weston-examples \
"
