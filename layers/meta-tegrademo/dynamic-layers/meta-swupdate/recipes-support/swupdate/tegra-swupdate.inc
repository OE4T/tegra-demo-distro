inherit l4t_version

# Set to "true" to use logic which only installs the bootloader
# when a change in L4T_VERSION is found between current and target rootfs
# When using this feature it's also recommended to use UBOOT_EXTLINUX
# as the boot mechanism and UBOOT_EXTLINUX_FDT.  Otherwise you need to force
# TEGRA_SWUPDATE_BOOTLOADER_VERSION mismatch whenever the devicetree
# changes.
# When using this feature It's also recommended to define
# TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER below
# in order to be able to recover from power off during capsule update scenarios
# without creating unbootable slots.
# Suggestions for using this feature:
# Add this content to your machine.conf or local .conf if using
# true for this feature
# UBOOT_EXTLINUX = "1"
# UBOOT_EXTLINUX_FDT = "/boot/${DTBFILE}"
# UBOOT_EXTLINUX_FDT = "${DTBFILE}"
# And define TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER below
TEGRA_SWUPDATE_BOOTLOADER_INSTALL_ONLY_IF_DIFFERENT ?= "false"


# The version written into the sw-versions file for the
# bootloader update capsule, used to control bootloader
# updates when TEGRA_SWUPDATE_BOOTLOADER_INSTALL_ONLY_IF_DIFFERENT is "true"
# Can be set to anything, but ideally would match the value
# used for get_hex_bsp_version in tegra-uefi-capsule-signing.bbclass
# to support comparisons with runtime checks of version in
# /sys/firmware/efi/esrt/entries/entry0/fw_version
TEGRA_SWUPDATE_BOOTLOADER_VERSION ?= "${L4T_VERSION}"


TEGRA_SWUPDATE_CAPSULE_INSTALL_PATH ?= "/boot/efi/EFI/UpdateCapsule/TEGRA_BL.Cap"

# Define the variable below to write a marker file at the location below appended with the slot number
# something like TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER ?= "/data/swupdate-capsule-update-slot-"
# which will be written:
#  * with -<slot>-inprogress suffix when a capsule update is in progress
#  * with -<slot> when capsule update is complete for a slot
# Please note:
#  * You must ensure this mountpoint is available when either slot is booted, for instance
#    using a data partition and/or read/write overlay or a dedicated partition.
#  * You should review the logic associated to mountpoint sequencing on the swupdate
#    service and genconfig script to ensure it works with your implementation.
#
TEGRA_SWUPDATE_LAST_CAPSULE_UPDATE_COMPLETE_SLOT_MARKER ?= ""
