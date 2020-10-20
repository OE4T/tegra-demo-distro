FILESEXTRAPATHS_prepend := "${THISDIR}/${BPN}:"

dirs755_append_tegrademo-mender = " /data"

RDEPENDS_${PN}_append_tegrademo-mender = " data-overlay-setup"
RRECOMMENDS_${PN}_append_tegrademo-mender = " kernel-module-overlay"
