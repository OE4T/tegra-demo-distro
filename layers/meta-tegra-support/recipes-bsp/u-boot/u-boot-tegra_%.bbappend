# Work around Mender's installation of this file (symlink)
# in its libubootenv bbappend.
do_install_append_mender-uboot() {
    rm -f ${D}${sysconfdir}/fw_env.config
}

