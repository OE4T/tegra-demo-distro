DESCRIPTION = "Tegra reference image with the Holoscan SDK, Holoscan Camera, their examples and tests, and Jetson IO"

require demo-image-reference.inc

python () {
    if 'meta-iceoryx2' not in d.getVar('BBFILE_COLLECTIONS').split():
        raise bb.parse.SkipRecipe('requires the meta-iceoryx2 layer')
}

CORE_IMAGE_BASE_INSTALL += " \
    packagegroup-demo-holoscan \
    packagegroup-demo-holoscan-tests \
    python3-jetson-io \
"

TOOLCHAIN_TARGET_TASK:remove = "packagegroup-demo-holoscan-tests python3-jetson-io"

TOOLCHAIN_HOST_TASK += "nativesdk-packagegroup-holoscan-sdk-host"

SDKIMAGE_FEATURES = "dev-pkgs"
