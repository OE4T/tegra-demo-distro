DESCRIPTION = "Holoscan SDK, Holoscan Camera and their examples and tests"

LICENSE = "MIT"

inherit packagegroup

PACKAGES = "${PN} ${PN}-tests"

RDEPENDS:${PN} = " \
    holoscan-sdk \
    python3-holoscan-sdk \
    holoscan-camera \
"

RDEPENDS:${PN}-tests = " \
    holoscan-sdk-benchmarks \
    holoscan-sdk-examples \
    holoscan-camera-examples \
    ${@bb.utils.contains('DISTRO_FEATURES', 'ptest', 'holoscan-sdk-ptest holoscan-camera-ptest', '', d)} \
"
