DESCRIPTION = "Partition layout for tegra-sysinstall"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

DEPENDS = "tegra-helper-scripts-native tegra-bootfiles"

COMPATIBLE_MACHINE = "(tegra)"

inherit python3native image_types_tegra

do_configure() {
    tegraflash_create_flash_config ${B} "dummy"
}

do_compile() {
    flashtype="sdmmc_user"
    if ${STAGING_BINDIR_NATIVE}/tegra186-flash/nvflashxmlparse -l flash.xml.in | tail -n "+2" | grep -q "sdcard"; then
        flashtype="sdcard"
    fi
    rm -f ${B}/layout.tmp
    ${STAGING_BINDIR_NATIVE}/tegra186-flash/nvflashxmlparse -t $flashtype flash.xml.in > ${B}/layout.tmp
    rm -f ${B}/partition_table
    touch ${B}/partition_table
    while read line; do
	  eval "$line"
	  if [ $partfilltoend -eq 1 ]; then
	      partsize="REMAIN"
	  fi
	  echo "$partnumber,$partname,$partsize,,$partguid,,$start_location" >> ${B}/partition_table
    done < ${B}/layout.tmp
}

do_install() {
    install -d ${D}${datadir}/tegra-sysinstall
    install -m 0644 ${B}/partition_table ${D}${datadir}/tegra-sysinstall/
}

FILES_${PN} = "${datadir}/tegra-sysinstall"
PACKAGE_ARCH = "${MACHINE_ARCH}"
