DESCRIPTION = "Install tegra fitImage in the location expected by u-boot"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

COMPATIBLE_MACHINE = "(cot)"

do_install() {
    fitImgPath=$(readlink -f ${DEPLOY_DIR_IMAGE}/fitImage)
    fitImgName=$(basename "$fitImgPath")
    install -d ${D}/boot
    install -m 0644 $fitImgPath ${D}/boot/
    ln -sf $fitImgName ${D}/boot/fitImage
}

do_install[depends] += "linux-tegra:do_deploy"
FILES:${PN} = "/boot/fitImage*"
PACKAGE_ARCH = "${MACHINE_ARCH}"
