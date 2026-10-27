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

# Virtualization packages: docker, nvidia-container-toolkit
# docker-data-conf and containerd-data-conf redirect storage to /data (requires data-partition)
CORE_IMAGE_BASE_INSTALL += " \
    docker \
    nvidia-container-toolkit \
    docker-registry-config \
    docker-data-conf \
    containerd-data-conf \
"

# shadow-securetty populates /etc/securetty from SERIAL_CONSOLES at build time
CORE_IMAGE_BASE_INSTALL += "shadow"
