DESCRIPTION = "Packagegroup for common Tegra demo test applications"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS_${PN} = " \
    cuda-samples \
    gpu-burn \
"
