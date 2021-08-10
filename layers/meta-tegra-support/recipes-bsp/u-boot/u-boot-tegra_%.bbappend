# Work around Mender's installation of this file (symlink)
# in its libubootenv bbappend.
do_install:append:mender-uboot() {
    rm -f ${D}${sysconfdir}/fw_env.config
}

