DESCRIPTION = "Packagegroup for inclusion in all Tegra demo images"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    procps \
    sshfs-fuse \
    strace \
    tegra-tools-tegrastats \
"
RDEPENDS:${PN}:append:tegra210 = " haveged"
