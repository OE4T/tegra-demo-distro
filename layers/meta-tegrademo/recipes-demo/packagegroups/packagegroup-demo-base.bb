DESCRIPTION = "Packagegroup for inclusion in all Tegra demo images"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    procps \
    sshfs-fuse \
    strace \
    tegra-tools-tegrastats \
    ${ENTROPY_HELPER} \
"
ENTROPY_HELPER = "rng-tools"
ENTROPY_HELPER:tegra210 = "haveged"
