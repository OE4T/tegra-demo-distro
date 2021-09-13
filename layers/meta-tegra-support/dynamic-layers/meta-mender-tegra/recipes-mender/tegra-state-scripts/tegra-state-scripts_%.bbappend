FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:remove = "file://redundant-boot-rollback-script-uboot"

copy_install_script() {
    sed -e's,@COPY_MACHINE_ID@,${PERSIST_MACHINE_ID},' ${S}/redundant-boot-install-script > ${MENDER_STATE_SCRIPTS_DIR}/ArtifactInstall_Leave_80_bl-update
}

copy_install_script:mender-uboot() {
    cp ${S}/redundant-boot-install-script-uboot ${MENDER_STATE_SCRIPTS_DIR}/ArtifactInstall_Leave_80_bl-update
    cp ${S}/redundant-boot-commit-check-script-uboot ${MENDER_STATE_SCRIPTS_DIR}/ArtifactCommit_Enter_80_bl-check-update
}

copy_other_scripts() {
    :
}

do_compile:tegra210() {
    cp ${S}/redundant-boot-install-script-uboot ${MENDER_STATE_SCRIPTS_DIR}/ArtifactInstall_Leave_80_bl-update
}
