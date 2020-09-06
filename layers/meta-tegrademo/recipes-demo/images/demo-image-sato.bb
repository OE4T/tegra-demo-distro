DESCRIPTION = "Tegra demo image with Sato, a mobile environment and visual style for \
mobile devices. The image supports X11 with a Sato theme, Pimlico \
applications, and contains terminal, editor, and file manager."

require demo-image-common.inc

IMAGE_FEATURES += "splash x11-base x11-sato hwcodecs"

CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-x11tests"
CORE_IMAGE_BASE_INSTALL += "${@bb.utils.contains('DISTRO_FEATURES', 'vulkan', 'packagegroup-demo-vulkantests', '', d)}"
