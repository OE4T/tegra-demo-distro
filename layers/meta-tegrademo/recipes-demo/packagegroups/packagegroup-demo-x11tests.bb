DESCRIPTION = "Tegra demo apps and tests for X11"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS_${PN} = " \
    cuda-samples \
    gstreamer-tests \
    l4t-graphics-demos-x11 \
    libgl-mesa \
    mesa-demos \
    nvgstapps \
"
