FILESEXTRAPATHS:prepend := "${THISDIR}/${BPN}:"
SRC_URI += "file://0001-Add-option-to-disable-build-path-searches-for-data-f.patch"

DEBUG_PREFIX_MAP += "\
 -fmacro-prefix-map=${WORKDIR}/contrib=/usr/src/debug/${PN}/${EXTENDPE}${PV}-${PR} \
 -fdebug-prefix-map=${WORKDIR}/contrib=/usr/src/debug/${PN}/${EXTENDPE}${PV}-${PR} \
"
PSEUDO_IGNORE_PATHS:append = ",${WORKDIR}/contrib"
EXTRA_OECMAKE += "-DOPENCV_DISABLE_BUILD_DIR_SEARCH_PATHS=ON"
