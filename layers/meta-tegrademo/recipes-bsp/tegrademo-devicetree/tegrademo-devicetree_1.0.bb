DESCRIPTION = "Meta-tegrademo example device trees for out-of-tree builds."
HOMEPAGE = "https://github.com/OE4T"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit devicetree

COMPATIBLE_MACHINE = "(tegra)"

DEPENDS += "nvidia-kernel-oot"

S = "${UNPACKDIR}"

SRC_URI = "\
    file://tegra234-p3737-0000+p3701-0000-oe4t.dts \
    file://tegra234-p3768-0000+p3767-0000-oe4t.dts \
"

DT_INCLUDE = " \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/tegra/nv-public \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/t23x/nv-public/include/kernel \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/t23x/nv-public/include/nvidia-oot \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/t23x/nv-public/include/platforms \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/t23x/nv-public \
    ${RECIPE_SYSROOT}/usr/src/device-tree/nvidia/t23x/nv-public/nv-platform \
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
