DESCRIPTION = "Full Tegra demo image with X11/Sato, nvidia-docker, OpenCV, \
VPI samples, TensorRT samples, and Tegra multimedia API sample apps."

require demo-image-common.inc

IMAGE_FEATURES += "splash x11-base x11-sato hwcodecs"

inherit features_check

REQUIRED_DISTRO_FEATURES = "x11 opengl virtualization"

CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-x11tests"
CORE_IMAGE_BASE_INSTALL += "${@bb.utils.contains('DISTRO_FEATURES', 'vulkan', 'packagegroup-demo-vulkantests', '', d)}"
CORE_IMAGE_BASE_INSTALL += "libvisionworks-devso-symlink nvidia-docker cuda-libraries tegra-mmapi-tests vpi1-tests tensorrt-tests"
