inherit l4t_version

# The version written into the sw-versions file for the
# bootloader update capsule.
# Can be set to anything, but ideally would match the value
# used for get_hex_bsp_version in tegra-uefi-capsule-signing.bbclass
# to support comparisons with runtime checks of version in
# /sys/firmware/efi/esrt/entries/entry0/fw_version, which
# is what the following default setting does.
TEGRA_SWUPDATE_BOOTLOADER_VERSION ?= "${L4T_VERSION}"

# The UEFI capsule updater expects to find capsules in directory
# \EFI\UpdateCapsule (in the Windows-style path naming
# that EFI uses) on the ESP partition. By default, the
# ESP is mounted at `/boot/efi` when Linux boots, but
# if your configuration is different, override the
# default setting.
TEGRA_SWUPDATE_CAPSULE_INSTALL_PATH ?= "/boot/efi/EFI/UpdateCapsule/TEGRA_BL.Cap"
