# Work around the global export of this variable
# that is added in mender-setup.bbclass
unset MENDER_MACHINE[export]
# and the addition of the variable to the whitelist
# which changes the signature for all tasks
BB_HASHBASE_WHITELIST_remove = "MENDER_MACHINE"

MENDER_DATA_PART_FSTAB_OPTS ?= "defaults,data=journal"
OS_RELEASE_VERSION ??= "${BUILDNAME}"

update_version_files () {
    dest="$1"
    if [ -f $dest/${sysconfdir}/mender/artifact_info -a -n "${MENDER_ARTIFACT_NAME}" ]; then
        echo "artifact_name=${MENDER_ARTIFACT_NAME}" > $dest/${sysconfdir}/mender/artifact_info
    fi

    if [ -f $dest/${sysconfdir}/os-release ]; then
        sed -i -r -e's,^VERSION=.*,VERSION="${OS_RELEASE_VERSION}",' \
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

ROOTFS_POSTPROCESS_COMMAND_append = " rootfs_version_info;"

PACKAGE_ARCH_pn-mender-client = "${MACHINE_ARCH}"
