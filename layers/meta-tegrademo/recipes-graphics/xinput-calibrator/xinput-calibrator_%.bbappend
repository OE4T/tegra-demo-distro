# Suppress autostart on non-touchscreen machines; Xsession.d/30xinput_calibrate.sh
# already gates on HAVE_TOUCHSCREEN correctly.
do_install:append() {
    if ${@bb.utils.contains('MACHINE_FEATURES', 'touchscreen', 'false', 'true', d)}; then
        rm -f ${D}${sysconfdir}/xdg/autostart/xinput_calibrator.desktop
    fi
}
