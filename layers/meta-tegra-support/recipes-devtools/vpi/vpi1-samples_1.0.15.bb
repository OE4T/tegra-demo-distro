SUMMARY = "NVIDIA VPI command-line sample applications"
HOMEPAGE = "https://developer.nvidia.com/embedded/vpi"
LICENSE = "BSD-3-Clause & Proprietary"
LIC_FILES_CHKSUM = "file://01-convolve_2d/main.cpp;beginline=4;endline=26;md5=0151558a559d381e69a909edafc3d247 \
                    file://assets/LICENSE;md5=6b5f633fc3acaabf21035790a05b1c71"

COMPATIBLE_MACHINE = "(tegra)"

inherit l4t_deb_pkgfeed cuda cmake

SRC_COMMON_DEBS = "vpi1-samples_${PV}_arm64.deb;subdir=vpi1-samples"
SRC_URI[sha256sum] = "98ea137962cb4bbfb1a778faf1cc3b19e27bbd0473aa7ab21cf9fde3a0469d9b"

SRC_URI += "file://CMakeLists.txt;subdir=vpi1-samples/opt/nvidia/vpi1/samples \
            file://0001-06-klt_tracker-minor-update-in-usage.patch"

VPI_PREFIX = "/opt/nvidia/vpi1"
EXTRA_OECMAKE = "-DCMAKE_INSTALL_PREFIX:PATH=${VPI_PREFIX}"

PACKAGECONFIG ??= "${@bb.utils.contains('LICENSE_FLAGS_WHITELIST', 'commercial', 'video', bb.utils.contains('LICENSE_FLAGS_WHITELIST', 'commercial_ffmpeg', 'video', '', d), d)}"
PACKAGECONFIG[video] = "-DBUILD_VIDEO_SAMPLES=ON,-DBUILD_VIDEO_SAMPLES=OFF,"

S = "${WORKDIR}/vpi1-samples/opt/nvidia/vpi1/samples"

DEPENDS = "libnvvpi1 opencv"

FILES_${PN} = "${VPI_PREFIX}"
