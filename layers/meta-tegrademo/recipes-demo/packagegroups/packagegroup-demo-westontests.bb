DESCRIPTION = "Packagegroup for Tegra demo weston test applications"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    gstreamer-tests \
    l4t-graphics-demos-wayland \
    weston-examples \
"
