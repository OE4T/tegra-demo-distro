PTEST_ENABLED = "0"

do_install:append() {
    sed -i -e's,^#user_allow_other,user_allow_other,' ${D}${sysconfdir}/fuse.conf
}
