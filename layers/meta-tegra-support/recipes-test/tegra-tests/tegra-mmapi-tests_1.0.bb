DESCRIPTION = "Scripts for testing Tegra Multimedia API"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_URI = "\
	file://run-mmapi-tests.sh \
"

COMPATIBLE_MACHINE = "(tegra)"

S = "${WORKDIR}"

do_compile() {
    :
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${S}/run-mmapi-tests.sh ${D}${bindir}/run-mmapi-tests
}

PACKAGE_ARCH = "${TEGRA_PKGARCH}"
RDEPENDS:${PN} = "tegra-mmapi-samples tegra-tools-jetson-clocks"
