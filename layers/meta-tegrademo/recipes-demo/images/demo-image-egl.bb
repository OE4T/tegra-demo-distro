DESCRIPTION = "Tegra demo image with no display/window manager."

require demo-image-common.inc

IMAGE_FEATURES += "hwcodecs"

inherit features_check

REQUIRED_DISTRO_FEATURES = "opengl"

CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-egltests"
