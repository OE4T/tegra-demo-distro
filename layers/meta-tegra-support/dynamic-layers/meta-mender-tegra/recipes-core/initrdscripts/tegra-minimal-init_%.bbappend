FILESEXTRAPATHS:prepend := "${THISDIR}/${BPN}:"

EXTRADEPS = ""
EXTRADEPS:tegra = "tegra-boot-tools-earlyboot"
EXTRADEPS:tegra210 = ""
RDEPENDS:${PN} += "${EXTRADEPS}"
