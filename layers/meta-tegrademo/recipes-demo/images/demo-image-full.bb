DESCRIPTION = "Full Tegra demo image with X11/Sato, nvidia-docker, OpenCV, \
VPI samples, TensorRT samples, and Tegra multimedia API sample apps."

require demo-image-common.inc

IMAGE_FEATURES += "splash x11-base x11-sato hwcodecs"

inherit features_check

REQUIRED_DISTRO_FEATURES = "x11 opengl"

CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-x11tests"
CORE_IMAGE_BASE_INSTALL += "${@bb.utils.contains('DISTRO_FEATURES', 'vulkan', 'packagegroup-demo-vulkantests', '', d)}"
CORE_IMAGE_BASE_INSTALL += "cuda-libraries tegra-mmapi-tests tensorrt-tests vpi-tests"

# tegra_docker is added by the meta-virtualization bbappend, which ships docker
TEST_SUITES:append = " tegra_gstreamer tegra_vulkan tegra_vpi tegra_mmapi \
                       tegra_camera tegra_opencv tegra_tensorrt \
                       tegra_deepstream \
                       tegra_capsule"
