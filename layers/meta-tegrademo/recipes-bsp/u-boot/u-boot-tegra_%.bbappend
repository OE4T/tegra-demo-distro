FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI_append_cot = " \
  file://enable-FIT-image-support.cfg \
"

RDEPENDS_${PN}_remove_cot = "${PN}-extlinux"
