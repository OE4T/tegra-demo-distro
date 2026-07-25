DESCRIPTION = "Packagegroup for inclusion in all Tegra demo images"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    gptfdisk \
    procps \
    sshfs-fuse \
    strace \
    tegra-tools-tegrastats \
"
