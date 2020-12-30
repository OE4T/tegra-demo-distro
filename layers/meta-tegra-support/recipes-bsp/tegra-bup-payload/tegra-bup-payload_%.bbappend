do_install_append_tegra186() {
    install -m 0644 ${DEPLOY_DIR_IMAGE}/${@bupfile_basename(d)}.full_init_only.bup-payload ${D}/opt/ota_package/full_init_payload
}

FILES_${PN}_append_tegra186 = " /opt/ota_package/full_init_payload"
RDEPENDS_${PN}_remove = "tegra-redundant-boot"
RDEPENDS_${PN}_append = " tegra-boot-tools-updater"

