DESCRIPTION = "Packagegroup for common Tegra demo test applications"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    cuda-samples \
    gpu-burn \
    optee-test-prebuilt \
"
