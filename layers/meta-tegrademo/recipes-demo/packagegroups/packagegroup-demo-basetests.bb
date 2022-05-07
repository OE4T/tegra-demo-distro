DESCRIPTION = "Packagegroup for common Tegra demo test applications"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    cuda-samples \
    gpu-burn \
"

RDEPENDS:${PN}:append:tegra194 = " optee-test-prebuilt"
