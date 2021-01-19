FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI_append = " \
  file://enable-FIT-image-support.cfg \
"

SRC_URI_append_tegra210 = " \
  file://0014-tegra210-bootm-Increase-CONFIG_SYS_BOOTM_LEN-to-64MB.patch \
  file://0015-Tegra210-Add-support-to-boot-with-FIT-image.patch \
  file://0016-tools-fit_check_sign.c-Update-usage-function.-Add-c-.patch \
"

RDEPENDS_${PN}_remove_cot = "${PN}-extlinux"
