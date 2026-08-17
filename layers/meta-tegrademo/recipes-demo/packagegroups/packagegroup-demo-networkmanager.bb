DESCRIPTION = "NetworkManager with WiFi support for images that use it as the primary network manager"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    networkmanager \
    networkmanager-wifi \
"

RDEPENDS:${PN}:append:tegra264 = " \
    networkmanager-config \
"
