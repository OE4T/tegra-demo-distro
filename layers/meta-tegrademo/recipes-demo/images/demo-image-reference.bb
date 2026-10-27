DESCRIPTION = "Tegra reference image with comprehensive test tools for QA validation. \
Includes all publicly available test packages from OE/Yocto recipes"

require demo-image-reference.inc

# EGL-device / headless multimedia tests (no window manager required)
CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-egltests"

# Additional public test tools: v4l-utils, lmbench, iperf3, rt-tests, perf, glmark2, kmscube
CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-reftests"

# Extra kernel modules for reference image test coverage (crypto self-test, UVC webcams)
CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-refmodules"

# Tegra-specific test packages (from public L4T source in meta-tegra / meta-tegra-community)
CORE_IMAGE_BASE_INSTALL += " \
    cuda-libraries \
    tegra-cuda-utils \
    cudnn-tests \
    tensorrt-tests \
    vpi4-tests \
    vpi4-samples \
    tegra-tools-dram-info \
    pva-sdk \
    nsight-systems \
"

# X11 packages: argus-samples, mesa-demos, l4t-graphics-demos-x11, SIPL, MMAPI
CORE_IMAGE_BASE_INSTALL += " \
    packagegroup-demo-x11tests \
    jetson-sipl-api \
    jetson-sipl-api-drivers \
    tegra-mmapi-tests \
"

# Vulkan packages: vulkan-tools, tegra-libraries-vulkan
CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-vulkantests"
