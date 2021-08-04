DESCRIPTION = "NVIDIA Tegra Multimedia API headers and examples"
HOMEPAGE = "http://developer.nvidia.com"
LICENSE = "Proprietary & BSD"

require recipes-multimedia/argus/tegra-mmapi-${PV}.inc

SRC_URI += "\
           file://jpeg-fixups.patch \
           file://cross-build-fixups.patch \
           file://vector-fixup.patch \
           file://make-getpixel-python3-compatible.patch \
           file://fix-dq-thread-race.patch \
           file://sample-bounding-box.txt \
           file://0001-Support-tegra_udrm-in-NvDrmRenderer.patch \
           "

DEPENDS = "libdrm tegra-mmapi virtual/egl virtual/libgles1 virtual/libgles2 jpeg expat gstreamer1.0 glib-2.0 v4l-utils tensorrt cudnn opencv"

LIC_FILES_CHKSUM = "file://LICENSE;md5=2cc00be68c1227a7c42ff3620ef75d05"

inherit pkgconfig cuda python3native

B = "${S}"

CLEANBROKEN = "1"

do_configure() {
    rm -f ${S}/include/nvbuf_utils.h
    find samples -name 'Makefile' -exec sed -i -e's,^LDFLAGS,NVLDFLAGS,' -e's,\$(LDFLAGS),$(LDFLAGS) $(NVLDFLAGS),' {} \;
}

do_compile() {
    export CPP="${@cuda_extract_compiler('CXX', d)[0]}"
    CXX_EXTRA="${@cuda_extract_compiler('CXX', d, prefix='')[1]}"
    export CUDA_PATH=${STAGING_DIR_NATIVE}/usr/local/cuda-${CUDA_VERSION}
    PATH=$CUDA_PATH/bin:$PATH
    export CPPFLAGS="${CXX_EXTRA} ${CXXFLAGS} -I${CUDA_PATH}/include"
    CPPFLAGS="$CPPFLAGS `pkg-config --cflags libdrm`"
    CPPFLAGS="$CPPFLAGS `pkg-config --cflags opencv4`"
    export LDFLAGS="-L${CUDA_PATH}/lib ${LDFLAGS}"
    CCBIN=`which $CPP`
    oe_runmake -j1 all TEGRA_ARMABI=${HOST_ARCH} TARGET_ROOTFS=${STAGING_DIR_HOST} NVCC=nvcc NVCCFLAGS="--shared -ccbin=${CCBIN}" GENCODE_FLAGS="${CUDA_NVCC_ARCH_FLAGS}" PYTHON="${PYTHON}"
}

do_install() {
    install -d ${D}/opt/tegra-mmapi
    cp -R --preserve=mode,timestamps ${S}/data ${D}/opt/tegra-mmapi/
    install -m 0644 ${WORKDIR}/sample-bounding-box.txt ${D}/opt/tegra-mmapi/data/
    install -d ${D}/opt/tegra-mmapi/bin
    install -m 0755 ${S}/samples/00_video_decode/video_decode ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/01_video_encode/video_encode ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/02_video_dec_cuda/video_dec_cuda ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/03_video_cuda_enc/video_cuda_enc ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/04_video_dec_trt/video_dec_trt ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/05_jpeg_encode/jpeg_encode ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/06_jpeg_decode/jpeg_decode ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/07_video_convert/video_convert ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/08_video_dec_drm/video_dec_drm ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/09_camera_jpeg_capture/camera_jpeg_capture ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/10_camera_recording/camera_recording ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/12_camera_v4l2_cuda/camera_v4l2_cuda ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/13_multi_camera/multi_camera ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/backend/backend ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/frontend/frontend ${D}/opt/tegra-mmapi/bin/
    install -m 0755 ${S}/samples/v4l2cuda/capture-cuda ${D}/opt/tegra-mmapi/bin/
}

FILES_${PN} += "/opt/tegra-mmapi"
RDEPENDS_${PN} += "tegra-libraries-libv4l-plugins"

