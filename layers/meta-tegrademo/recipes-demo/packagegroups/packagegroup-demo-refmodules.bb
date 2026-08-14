DESCRIPTION = "Extra kernel modules for Tegra reference image test coverage"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    kernel-module-tcrypt \
    kernel-module-uvcvideo \
"

# Built into linux-yocto's default config rather than modules; recommend
# instead of require so kernels that do module them (e.g. noble) still get them.
RRECOMMENDS:${PN} = " \
    kernel-module-ccm \
    kernel-module-cmac \
    kernel-module-ctr \
    kernel-module-gcm \
    kernel-module-ghash-generic \
    kernel-module-xts \
"
