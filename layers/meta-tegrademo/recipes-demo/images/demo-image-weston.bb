SUMMARY = "Tegra demo image with Weston compositor"

require demo-image-common.inc

IMAGE_FEATURES += "hwcodecs weston"

inherit features_check extrausers

EXTRA_USERS_PARAMS = "\
    usermod -a -G audio weston; \
"

REQUIRED_DISTRO_FEATURES = "wayland opengl"

CORE_IMAGE_BASE_INSTALL += "gtk+3-demo packagegroup-demo-westontests"
CORE_IMAGE_BASE_INSTALL += "${@bb.utils.contains('DISTRO_FEATURES', 'x11', 'weston-xwayland matchbox-terminal packagegroup-demo-x11tests', '', d)}"
CORE_IMAGE_BASE_INSTALL += "${@bb.utils.contains('DISTRO_FEATURES', 'vulkan', 'packagegroup-demo-vulkantests', '', d)}"
CORE_IMAGE_BASE_INSTALL += "${@bb.utils.contains('DISTRO_FEATURES', 'pulseaudio', 'pulseaudio-server pulseaudio-misc', '', d)}"
SYSTEMD_DEFAULT_TARGET = "graphical.target"

TEST_SUITES:append = " tegra_gstreamer tegra_vulkan tegra_camera"
