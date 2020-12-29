do_install_append() {
    ln -sf /run/tegra-nv-bootctrl/nv_boot_control.conf ${D}${sysconfdir}/
}
