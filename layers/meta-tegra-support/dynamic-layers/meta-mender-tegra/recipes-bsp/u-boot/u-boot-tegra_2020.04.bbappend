FILESEXTRAPATHS_prepend := "${THISDIR}/patches:"

SRC_URI_append_mender-uboot = " \
    file://0012-p3541-0000_defconfig-Mender-patch.patch \
    file://0015-Update-TX1-nano-emmc-defconfigs-for-new-UBENV-locati.patch \
    file://0017-Jetson-Xavier-NX-TX2-NX-mender.patch \
"
MENDER_UBOOT_ENV_STORAGE_DEVICE_OFFSET_tegra210 = "${@'3866624' if (d.getVar('TEGRA_SPIFLASH_BOOT') or '') == '1' else '3801088'}"
