DESCRIPTION = "Packagegroup for common Tegra demo test applications"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    cuda-samples \
    optee-nvsamples \
    optee-test \
"
