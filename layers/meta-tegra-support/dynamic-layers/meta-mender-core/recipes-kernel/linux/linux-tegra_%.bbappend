# Undo the following additions made by meta-mender-core,
# which does not apply to tegra platforms
SRC_URI_remove_mender-grub = "${@if_kernel_recipe(' file://enable_efi_stub.cfg', '', d)}"

# Rather ugly hack to ensure that meta-mender-core's files directory
# is also removed from consideration, since linux-yocto.bbclass adds
# all directories that contain config fragments into its file-cksums
# list, which needlessly (for us) changes the task hash.
python() {
    extrapaths = d.getVar('FILESEXTRAPATHS').split(':')
    newpaths = ':'.join([path for path in extrapaths if not path.endswith('meta-mender-core/recipes-kernel/linux/files')])
    d.setVar('FILESEXTRAPATHS', newpaths)
}
