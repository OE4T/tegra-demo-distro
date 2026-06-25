DESCRIPTION = "Meta-tegrademo example device trees for out-of-tree builds."
HOMEPAGE = "https://github.com/OE4T"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit tegra-devicetree

COMPATIBLE_MACHINE = "(tegra)"

S = "${UNPACKDIR}"

SRC_URI:tegra234 = "\
    file://tegra234-p3737-0000+p3701-0000-oe4t.dts \
    file://tegra234-p3768-0000+p3767-0000-oe4t.dts \
    file://tegra234-p3768-0000+p3767-0005-oe4t.dts \
"

SRC_URI:tegra264 = "\
    file://tegra264-p4071-0000+p3834-0008-oe4t.dts \
    file://tegra264-p4071-0000+p3834-0000-oe4t.dts \
"
