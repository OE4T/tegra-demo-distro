DESCRIPTION = "Simple example program demonstrating the use of EGLStreams with DRM KMS."
HOMEPAGE = "https://github.com/aritger"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING;md5=2c4ffb74754562207b887a66a37aad6c"

DEPENDS = "libdrm virtual/egl"

SRC_REPO ?= "github.com/madisongh/eglstreams-kms-example"
SRCBRANCH ?= "master"
SRC_URI = "git://${SRC_REPO};branch=${SRCBRANCH};protocol=https"
SRCREV = "${AUTOREV}"
PV = "1.0+git${SRCPV}"

COMPATIBLE_MACHINE = "(tegra)"
PACKAGE_ARCH_tegra = "${TEGRA_PKGARCH}"

S = "${WORKDIR}/git"

inherit pkgconfig

do_install() {
    oe_runmake install DESTDIR="${D}"
}
