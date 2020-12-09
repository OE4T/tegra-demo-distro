# XXX --- Temporary until these changes go upstream
MENDER_UBOOT_ENV_STORAGE_DEVICE_OFFSET_tegra210 = "${@'3866624' if (d.getVar('TEGRA_SPIFLASH_BOOT') or '') == '1' else '3801088'}"
# --- XXX
