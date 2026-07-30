DESCRIPTION = "System utilities for the Tegra reference image: GNU userland, hardware inspection, and system monitoring"

LICENSE = "MIT"

inherit packagegroup

# GNU userland — replaces busybox applets not covered by coreutils alone
RDEPENDS:${PN} = " \
    coreutils \
    findutils \
    sed \
    grep \
    gawk \
    bash \
    tar \
    gzip \
    bzip2 \
    xz \
    diffutils \
    patch \
    which \
    bc \
    util-linux \
    file \
    vim \
    minicom \
"

# Networking
RDEPENDS:${PN} += " \
    curl \
    rsync \
    iproute2 \
    iproute2-ss \
    iproute2-tc \
    iproute2-bridge \
    iproute2-nstat \
    iproute2-devlink \
    iputils \
    net-tools \
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
    e2fsprogs \
    psmisc \
    valgrind \
    python3-pip \
    usleep \
"

# Audio: PulseAudio daemon, pactl and other control utilities, full ALSA utils suite
RDEPENDS:${PN} += "${@bb.utils.contains('DISTRO_FEATURES', 'pulseaudio', 'pulseaudio-server pulseaudio-misc pulseaudio-pactl', '', d)}"
RDEPENDS:${PN} += "alsa-utils"

# RT kernel tools (chrt and taskset come from util-linux above)
RDEPENDS:${PN} += " \
    tuna \
    trace-cmd \
"
