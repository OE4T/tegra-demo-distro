SUMMARY = "Tegra swupdate update image"
DESCRIPTION = "A swupdate image for demonstrating tegra updates"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_URI = "\
    file://sw-description \
"

inherit swupdate image_types_tegra

require dynamic-layers/meta-swupdate/recipes-support/swupdate/tegra-swupdate.inc

ROOTFS_DEVICE_PATH ?= "/dev/disk/by-partlabel"

# ESP (EFI System Partition) archive for non-minimal boot builds.
# In non-minimal builds, BOOTAA64.efi (L4TLauncher) lives on the ESP and
# must be kept in sync with the firmware via OTA.  In minimal-boot builds,
# L4TLauncher is compiled into the UEFI image itself and the ESP file is
# absent, so this entry must be omitted from both the .swu CPIO and the
# sw-description to avoid swupdate errors.
ESP_ARCHIVE = "${TEGRA_ESP_IMAGE}-${MACHINE}.tar.gz"

def optional_esp_update(d):
    if bb.utils.to_boolean(d.getVar('TEGRA_MINIMAL_BOOT')):
        return ""
    archive = d.getVar('ESP_ARCHIVE')
    version = d.getVar('TEGRA_SWUPDATE_BOOTLOADER_VERSION')
    return f""",
    {{
        filename = "{archive}";
        type = "archive";
        installed-directly = true;
        path = "/boot/efi";
        name = "tegra-bootloader-capsule";
        version = "{version}";
    }}"""

OPTIONAL_ESP_UPDATE = "${@optional_esp_update(d)}"

# By default, infer the image name from our recipe name. To create
# a recipe for a swupdate based off an image, just create
# '<imagename>-swupdate.bb' and have it include this .inc file
SWUPDATE_CORE_IMAGE_NAME ?= "${@d.getVar('BPN').replace('-swupdate', '')}"

ROOTFS_FILENAME ?= "${SWUPDATE_CORE_IMAGE_NAME}-${MACHINE}.rootfs.tar.gz"

# images to build before building swupdate image. For any non image depends, add to the do_swuimage[depends] instead.
IMAGE_DEPENDS = "${SWUPDATE_CORE_IMAGE_NAME}"
IMAGE_DEPENDS:append = "${@' tegra-espimage' if not bb.utils.to_boolean(d.getVar('TEGRA_MINIMAL_BOOT')) else ''}"

# images and files that will be included in the .swu image
SWUPDATE_IMAGES = "${ROOTFS_FILENAME} tegra-bl.cap tegra-swupdate-script.lua"
SWUPDATE_IMAGES:append = "${@' ' + d.getVar('ESP_ARCHIVE') if not bb.utils.to_boolean(d.getVar('TEGRA_MINIMAL_BOOT')) else ''}"

# All non-image related depends go here
do_swuimage[depends] += "tegra-uefi-capsules:do_deploy"
do_swuimage[depends] += "tegra-swupdate-script:do_deploy"
do_swuimage[depends] += "${@'tegra-espimage:do_image_complete' if not bb.utils.to_boolean(d.getVar('TEGRA_MINIMAL_BOOT')) else ''}"

# Add a link using the core image name.swu to the resulting swu image
do_swuimage:append() {
    os.symlink(d.getVar("IMAGE_NAME") + ".swu", d.getVar("SWUPDATE_CORE_IMAGE_NAME") + "-" + d.getVar("MACHINE") + ".swu")
}
