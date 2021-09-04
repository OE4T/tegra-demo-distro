DESCRIPTION = "Scripts for testing Tegra VPI samples"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_URI = "\
    file://run-vpi1-tests.sh \
"

COMPATIBLE_MACHINE = "(tegra)"

S = "${WORKDIR}"


do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${S}/run-vpi1-tests.sh ${D}${bindir}/run-vpi1-tests
}

PACKAGE_ARCH = "${TEGRA_PKGARCH}"
RDEPENDS_${PN} = "vpi1-samples tegra-tools-jetson-clocks"
