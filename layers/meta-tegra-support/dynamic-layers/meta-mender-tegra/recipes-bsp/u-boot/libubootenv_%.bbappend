# XXX --- Temporary until these changes go upstream
MENDER_UBOOT_ENV_STORAGE_DEVICE_OFFSET:tegra210 = "${@'3866624' if (d.getVar('TEGRA_SPIFLASH_BOOT') or '') == '1' else '3801088'}"
# --- XXX

# Mender, for some reason, decided that libubootenv should supply the
# fw_env.config file, rather than keeping libubootenv generic and
# having the already platform-dependent u-boot recipe supply both
# that config file and the initial environment file, as was intended.
# We'll need the initial environment file to support bootloader
# updates that relocate the u-boot environment storage location,
# so remove this RPROVIDES so it can be supplied by the u-boot
# recipe.  The config file is still provided by this recipe,
# however.
RPROVIDES:${PN}:remove:tegra = "u-boot-default-env"

# Also stash an extra copy of the fw_env.config file in the
# rootfs so we can compare it to the currently-installed one
# in a state script, to see if we need to take steps to save
# and restore u-boot environment variables during a bootloader
# update.
do_install:append:tegra() {
    install -d ${D}${datadir}/u-boot
    install -m 0644 ${WORKDIR}/fw_env.config ${D}${datadir}/u-boot/
}
FILES:${PN}:append:tegra = " ${datadir}/u-boot"
