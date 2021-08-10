FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI:append:cot = " \
  file://enable-fitimage-support.cfg \
  ${@'file://enable-fitimage-signing.cfg' if d.getVar('UBOOT_SIGN_ENABLE') == '1' else ''} \
"
SRC_URI:append:cot:mender-uboot = " file://0018-env-enable-fit-image-support-with-mender.patch"

RDEPENDS:${PN}:remove:cot = "${PN}-extlinux"

do_deploy:append:cot() {
  if [ "${UBOOT_SIGN_ENABLE}" = "1" -a -n "${UBOOT_DTB_BINARY}" ] ; then
    uboot_deployed_image="${DEPLOYDIR}/${UBOOT_IMAGE}"
    rm -f ${DEPLOYDIR}/u-boot-${MACHINE}*.backup
    mv ${uboot_deployed_image} ${uboot_deployed_image}.backup
    rm -f ${B}/initrd
    touch ${B}/initrd
    ${STAGING_BINDIR_NATIVE}/${SOC_FAMILY}-flash/mkbootimg \
      --kernel ${uboot_deployed_image}.backup \
      --ramdisk ${B}/initrd --cmdline "" \
      --board "${UBOOT_BOOTIMG_BOARD}" \
      --output ${uboot_deployed_image}
    rm -f ${B}/initrd
    rm -f ${uboot_deployed_image}.backup
  fi
}
