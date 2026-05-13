DESCRIPTION = "Meta-tegrademo example device trees for out-of-tree builds."
HOMEPAGE = "https://github.com/OE4T"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

TEGRA_UEFI_SIGNING_CLASS ??= "tegra-uefi-signing"

inherit ${TEGRA_UEFI_SIGNING_CLASS}
inherit devicetree deploy

PROVIDES = "virtual/dtb"

COMPATIBLE_MACHINE = "(tegra)"

DEPENDS += "nvidia-kernel-oot"

SRC_URI = "\
    file://tegra234-p3737-0000+p3701-0000-oe4t.dts \
    file://tegra234-p3768-0000+p3767-0000-oe4t.dts \
"

DT_INCLUDE = " \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/tegra/nv-public \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/t23x/nv-public/include/kernel \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/t23x/nv-public/include/nvidia-oot \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/t23x/nv-public/include/platforms \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/t23x/nv-public/nv-platform \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/t23x/nv-public \
    ${S} \
    ${KERNEL_INCLUDE} \
"

# From kernel-devicetree/generic-dts/Makefile
DTC_PPFLAGS:append = " -DLINUX_VERSION=600 -DTEGRA_HOST1X_DT_VERSION=2"

# re-implement function from devicetree.bbclass to preserve order of KERNEL_INCLUDE
def expand_includes(varname, d):
    import glob
    includes = list()
    # expand all includes with glob
    for i in (d.getVar(varname) or "").split():
        for g in glob.glob(i):
            if os.path.isdir(g): # only add directories to include path
                includes.append(g)
    return includes

# The default signing class won't sign DTBs not in the L4T sources,
# so define our own here.
#
do_sign_dtbs() {
    for dtb in ${KERNEL_DEVICETREE}; do
        local dtbf="${B}/$dtbf"
        if [ -f "$dtbf" ]; then
            tegra_uefi_attach_sign "$dtbf"
        fi
    done
}
do_sign_dtbs[dirs] = "${B}"
do_sign_dtbs[depends] += "${TEGRA_UEFI_SIGNING_TASKDEPS}"
do_sign_dtbs[file-checksums] += "${TEGRA_UEFI_SIGNING_FILECHECKSUMS}"

addtask sign_dtbs after do_compile before do_install

# The devicetree class automatically installs and deploys *.dtb and *.dtbo
# files, but we need to install/deploy any signed files, if they exist
#
do_install:append() {
    for dtb in ${KERNEL_DEVICETREE}; do
        local dtbf="${B}/$dtb.signed"
        if [ -f "$dtbf" ]; then
            install -m 0644 "$dtbf" ${D}/boot/devicetree
        fi
    done
}

FILES:${PN} += " \
    /boot/devicetree/* \
"

do_deploy:append() {
    for dtb in ${KERNEL_DEVICETREE}; do
        local dtbf="${B}/$dtb.signed"
        if [ -f "$dtbf" ]; then
            install -m 0644 "$dtbf" ${DEPLOYDIR}/devicetree
        fi
    done
}
