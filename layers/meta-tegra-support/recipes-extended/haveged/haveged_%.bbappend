do_install_append() {
    sed -i -e's!^PrivateTmp=true!PrivateTmp=false!' \
           -e's!^PrivateDevices=true!PrivateDevices=false!' ${D}${systemd_system_unitdir}/haveged.service
}
