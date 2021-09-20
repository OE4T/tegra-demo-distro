FILESEXTRAPATHS_prepend := "${THISDIR}/${BPN}:"

EXTRADEPS = ""
EXTRADEPS_tegra = "tegra-boot-tools-earlyboot"
EXTRADEPS_tegra210 = ""
RDEPENDS_${PN} += "${EXTRADEPS}"
