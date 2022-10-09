FILESEXTRAPATHS:prepend := "${THISDIR}/${BPN}:"
SRC_URI += "file://0001-Add-option-to-disable-build-path-searches-for-data-f.patch"

EXTRA_OECMAKE += "-DOPENCV_DISABLE_BUILD_DIR_SEARCH_PATHS=ON"
