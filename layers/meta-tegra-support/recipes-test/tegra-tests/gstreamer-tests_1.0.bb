DESCRIPTION = "Scripts for testing gstreamer playback and capture"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_URI = "\
	https://peach.themazzone.com/durian/trailer/sintel_trailer-1080p.mp4 \
	file://sinteltest.sh.in \
	file://capturetest.sh.in \
	file://nvjpegtest.sh.in \
	file://confvars.in \
"
# The above mirror is more reachable than download.blender.org
SRC_URI[md5sum] = "bfd19c4e7ad04c72bfb327cf7e6b9576"
SRC_URI[sha256sum] = "34bbd52a4b89fdf63c8ace50b268da26653a59508288100cd3c23de276db7931"

S = "${WORKDIR}"
B = "${WORKDIR}/build"

do_compile() {
    for f in sinteltest.sh capturetest.sh nvjpegtest.sh confvars; do
	sed -e's,@DATADIR@,${datadir},g' \
	    ${S}/${f}.in > ${B}/${f}
    done
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${B}/sinteltest.sh ${D}${bindir}/sinteltest
    install -m 0755 ${B}/capturetest.sh ${D}${bindir}/capturetest
    install -m 0755 ${B}/nvjpegtest.sh ${D}${bindir}/nvjpegtest
    install -d ${D}${datadir}/gstreamer-tests
    install -m 0644 ${B}/confvars ${D}${datadir}/gstreamer-tests/confvars
    install -m 0644 ${S}/sintel_trailer-1080p.mp4 ${D}${datadir}/gstreamer-tests
}

PACKAGE_ARCH = "${MACHINE_ARCH}"
RDEPENDS_${PN} = "gst-player gstreamer1.0 gstreamer1.0-plugins-nveglgles gstreamer1.0-plugins-base-videotestsrc \
                  gstreamer1.0-plugins-nvvideo4linux2 gstreamer1.0-plugins-nvvideosinks gstreamer1.0-plugins-nvjpeg \
                  gstreamer1.0-plugins-nvvidconv gstreamer1.0-plugins-good-imagefreeze gstreamer1.0-plugins-bad-waylandsink \
                  gstreamer1.0-plugins-good-video4linux2 gstreamer1.0-plugins-nvdrmvideosink"
