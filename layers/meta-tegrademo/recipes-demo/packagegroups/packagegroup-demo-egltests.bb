DESCRIPTION = "Packagegroup for Tegra demo apps with no window manager"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS_${PN} = " \
    eglstreams-kms-example \
    l4t-graphics-demos-egldevice \
    tegra-udrm-probeconf \
"
