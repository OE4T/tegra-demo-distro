DESCRIPTION = "Packagegroup for Tegra demo apps with no window manager"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    eglstreams-kms-example \
    gstreamer-tests \
    l4t-graphics-demos-egldevice \
    tegra-udrm-probeconf \
"
