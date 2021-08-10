DESCRIPTION = "Packagegroup for inclusion in all Tegra demo images"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    haveged \
    procps \
    sshfs-fuse \
    strace \
    tegra-tools-tegrastats \
"
