DESCRIPTION = "Packagegroup for demo images using systemd.  These pacakges \
are not strictly required for systemd support, but provide tools that make \
using systemd easier."

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    less \
    systemd-analyze \
"

RDEPENDS:${PN}:append:tegra264 = " \
    systemd-networkd-config \
"
