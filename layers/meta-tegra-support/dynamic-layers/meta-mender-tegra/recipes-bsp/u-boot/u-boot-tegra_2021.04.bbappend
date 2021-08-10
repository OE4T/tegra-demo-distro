FILESEXTRAPATHS:prepend := "${THISDIR}/patches:"
# New for R32.4.4
SRC_URI:append:mender-uboot = " file://0012-p3541-0000_defconfig-Mender-patch.patch"
# XXX --- Temporary until these changes go upstream
SRC_URI:append:mender-uboot = " file://0015-Update-TX1-nano-emmc-defconfigs-for-new-UBENV-locati.patch"
SRC_URI:append:mender-uboot = " file://0016-Update-env-for-SPIflash-Nanos-for-R32.5.0-with-Mende.patch"
# New for R32.5.1
SRC_URI:append:mender-uboot = " file://0017-Jetson-Xavier-NX-TX2-NX-mender.patch"

MENDER_UBOOT_ENV_STORAGE_DEVICE_OFFSET:tegra210 = "${@'3997696' if (d.getVar('TEGRA_SPIFLASH_BOOT') or '') == '1' else '3801088'}"
# --- XXX
