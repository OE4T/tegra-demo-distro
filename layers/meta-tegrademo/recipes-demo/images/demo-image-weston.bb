SUMMARY = "Tegra demo image with Weston compositor"

require demo-image-common.inc

IMAGE_FEATURES += "hwcodecs"

inherit features_check

REQUIRED_DISTRO_FEATURES = "wayland opengl"

CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-weston packagegroup-demo-westontests"
CORE_IMAGE_BASE_INSTALL += "${@bb.utils.contains('DISTRO_FEATURES', 'x11', 'packagegroup-demo-x11tests', '', d)}"
CORE_IMAGE_BASE_INSTALL += "${@bb.utils.contains('DISTRO_FEATURES', 'vulkan', 'packagegroup-demo-vulkantests', '', d)}"
