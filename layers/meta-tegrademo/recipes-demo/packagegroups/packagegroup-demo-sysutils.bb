DESCRIPTION = "System utilities for the Tegra reference image: base utilities, hardware inspection, and system monitoring"

LICENSE = "MIT"

inherit packagegroup

# Base utilities should be provided by VIRTUAL-RUNTIME_base-utils

# Additional interactive tools
RDEPENDS:${PN} = " \
    bc \
    vim \
    minicom \
"

# Networking
RDEPENDS:${PN} += " \
    curl \
    rsync \
    iproute2-ss \
    iproute2-tc \
    iproute2-bridge \
    iproute2-nstat \
    iproute2-devlink \
    iputils \
    ethtool \
    iw \
"

# Hardware inspection
RDEPENDS:${PN} += " \
    pciutils \
    usbutils \
    i2c-tools \
    libgpiod-tools \
    spidev-test \
    can-utils \
    dmidecode \
    hdparm \
    nvme-cli \
    ufs-utils \
    devmem2 \
    lua \
"

# System monitoring and admin
RDEPENDS:${PN} += " \
    lsof \
    sysstat \
    valgrind \
    python3-pip \
    usleep \
"

# Audio: PulseAudio daemon, pactl and other control utilities, full ALSA utils suite
RDEPENDS:${PN} += "${@bb.utils.contains('DISTRO_FEATURES', 'pulseaudio', 'pulseaudio-server pulseaudio-misc pulseaudio-pactl', '', d)}"
RDEPENDS:${PN} += "alsa-utils"

# RT kernel tools (chrt and taskset come from the base utilities)
RDEPENDS:${PN} += " \
    tuna \
    trace-cmd \
"
