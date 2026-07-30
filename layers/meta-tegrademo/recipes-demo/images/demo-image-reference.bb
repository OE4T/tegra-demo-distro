DESCRIPTION = "Tegra reference image with comprehensive test tools for QA validation. \
Includes all publicly available test packages from OE/Yocto recipes"

require demo-image-common.inc

inherit features_check

REQUIRED_DISTRO_FEATURES = "opengl wayland wifi x11 vulkan virtualization overlayfs pulseaudio"

IMAGE_FEATURES += "hwcodecs x11-base x11-sato container-registry"

SYSTEMD_DEFAULT_TARGET = "graphical.target"

# Other convenient support packages
CORE_IMAGE_BASE_INSTALL += " \
    l4t-usb-device-mode \
    data-partition \
"

# System utilities: GNU userland, hardware inspection, networking, monitoring
CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-sysutils"

# NetworkManager with WiFi and TUI for headless configuration
# networkmanager-nmtui is pulled in via RRECOMMENDS when the nmtui PACKAGECONFIG is active
CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-networkmanager"

# Weston compositor (manual launch only, no weston-init service)
# weston RRECOMMENDS weston-init; suppress it so the service does not auto-start
# and conflict with the X11 session.
BAD_RECOMMENDATIONS += "weston-init"
CORE_IMAGE_BASE_INSTALL += " \
    weston \
    packagegroup-demo-westontests \
"

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

# Virtualization packages: docker, nvidia-container-toolkit
CORE_IMAGE_BASE_INSTALL += " \
    docker \
    nvidia-container-toolkit \
    docker-registry-config \
"

# shadow-securetty populates /etc/securetty from SERIAL_CONSOLES at build time
CORE_IMAGE_BASE_INSTALL += "shadow"
