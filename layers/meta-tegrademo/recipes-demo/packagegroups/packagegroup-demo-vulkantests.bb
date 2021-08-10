DESCRIPTION = "Packagegroup for common Tegra demo Vulkan test apps"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    vulkan-tools \
"
