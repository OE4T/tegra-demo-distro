# Work around the global export of this variable
# that is added in mender-setup.bbclass
unset MENDER_MACHINE[export]
# and the addition of the variable to the whitelist
# which changes the signature for all tasks
BB_HASHBASE_WHITELIST:remove = "MENDER_MACHINE"

DISTRO_FEATURES_BACKFILL:remove = "systemd"

BBMASK += "/meta-mender-core/recipes-devtools/e2fsprogs/"
BBMASK += "/meta-mender-core/recipes-core/systemd/"

MENDER_DATA_PART_FSTAB_OPTS ?= "defaults,data=journal"
OS_RELEASE_VERSION ??= "${BUILDNAME}"

update_version_files () {
    dest="$1"
    if [ -f $dest/${sysconfdir}/mender/artifact_info -a -n "${MENDER_ARTIFACT_NAME}" ]; then
        echo "artifact_name=${MENDER_ARTIFACT_NAME}" > $dest/${sysconfdir}/mender/artifact_info
    fi

    if [ -f $dest/${sysconfdir}/os-release ]; then
        sed --follow-symlinks -i -r -e's,^VERSION=.*,VERSION="${OS_RELEASE_VERSION}",' \
	    -e's,^VERSION_ID=.*,VERSION_ID="${BUILDNAME}",' \
	    -e's,^PRETTY_NAME=.*,PRETTY_NAME="${DISTRO_NAME} ${BUILDNAME}",' \
	    $dest/${sysconfdir}/os-release
    fi

    if [ -f $dest/${sysconfdir}/issue ]; then
        printf "%s \\%s \\l\n\n" "${DISTRO_NAME} ${BUILDNAME}" "n" >$dest/${sysconfdir}/issue
    fi

    if [ -f $dest/${sysconfdir}/issue.net ]; then
        printf "%s %%h\n\n" "${DISTRO_NAME} ${BUILDNAME}" >$dest/${sysconfdir}/issue.net
    fi
}

rootfs_version_info() {
    update_version_files ${IMAGE_ROOTFS}
}

ROOTFS_POSTPROCESS_COMMAND:append = " rootfs_version_info;"

PACKAGE_ARCH:pn-mender-client = "${MACHINE_ARCH}"

# mender-setup-image adds kernel-image and kernel-devicetree
# to MACHINE_ESSENTIAL_EXTRA_RDEPENDS, but they should *not*
# be included by default on cboot platforms.
MACHINE_ESSENTIAL_EXTRA_RDEPENDS:remove:tegra194 = "kernel-image kernel-devicetree"
MACHINE_ESSENTIAL_EXTRA_RDEPENDS:remove:tegra186 = "${@'kernel-image kernel-devicetree' if (d.getVar('PREFERRED_PROVIDER_virtual/bootloader') or '').startswith('cboot') else ''}"

# Not including jetson-nano-qspi-sd here due to major changes in
# the flash layout in L4T R32.5.0.
MENDER_DEVICE_TYPES_COMPATIBLE:append_jetson-tx1-devkit = " jetson-tx1"
MENDER_DEVICE_TYPES_COMPATIBLE:append_jetson-tx2-devkit = " jetson-tx2"
MENDER_DEVICE_TYPES_COMPATIBLE:append_jetson-tx2-devkit-tx2i = " jetson-tx2i"
MENDER_DEVICE_TYPES_COMPATIBLE:append_jetson-tx2-devkit-4gb = " jetson-tx2-4gb"
MENDER_DEVICE_TYPES_COMPATIBLE:append_jetson-agx-xavier-devkit = " jetson-xavier"
MENDER_DEVICE_TYPES_COMPATIBLE:append_jetson-agx-xavier-devkit-8gb = " jetson-xavier-8gb"
MENDER_DEVICE_TYPES_COMPATIBLE:append_jetson-nano-devkit-emmc = " jetson-nano-emmc"
