DESCRIPTION = "Meta-tegrademo example device trees for out-of-tree builds."
HOMEPAGE = "https://github.com/OE4T"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit devicetree

COMPATIBLE_MACHINE = "(tegra)"

SRC_URI = "\
    file://tegra194-p2888-0001-p2822-0000-oe4t.dts \
    file://tegra194-p3668-all-p3509-0000-oe4t.dts \
"

KERNEL_INCLUDE = " \
    ${STAGING_KERNEL_DIR}/nvidia/soc/tegra/kernel-include \
    ${STAGING_KERNEL_DIR}/nvidia/platform/tegra/common/kernel-dts \
    ${STAGING_KERNEL_DIR}/nvidia/soc/t19x/kernel-include \
    ${STAGING_KERNEL_DIR}/nvidia/soc/t19x/kernel-dts \
    ${STAGING_KERNEL_DIR}/nvidia/platform/t19x/common/kernel-dts \
    ${STAGING_KERNEL_DIR}/nvidia/soc/t23x/kernel-include \
    ${STAGING_KERNEL_DIR}/nvidia/soc/t23x/kernel-dts \
    ${STAGING_KERNEL_DIR}/nvidia/platform/t23x/common/kernel-dts \
    ${STAGING_KERNEL_DIR}/nvidia/platform/t19x/galen/kernel-dts \
    ${STAGING_KERNEL_DIR}/nvidia/platform/t19x/jakku/kernel-dts \
    ${STAGING_KERNEL_DIR}/nvidia/platform/t19x/mccoy/kernel-dts \
    ${STAGING_KERNEL_DIR}/nvidia/platform/t23x/concord/kernel-dts \
    ${STAGING_KERNEL_DIR}/scripts/dtc/include-prefixes \
"

# Straight from arch/arm64/boot/dts in kernel source tree
DTC_PPFLAGS:append = " -DLINUX_VERSION=504 -DTEGRA_HOST1X_DT_VERSION=1"

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
