IMAGE_FEATURES += "ssh-server-openssh"

LICENSE = "MIT"

inherit core-image

CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-base packagegroup-demo-basetests"
CORE_IMAGE_BASE_INSTALL += "${@'packagegroup-demo-systemd' if d.getVar('VIRTUAL-RUNTIME_init_manager') == 'systemd' else ''}"
# ship the L4T release-identity file (only the container toolkit pulls it otherwise)
CORE_IMAGE_BASE_INSTALL += "nv-tegra-release"
TOOLCHAIN_HOST_TASK += "nativesdk-packagegroup-cuda-sdk-host"

# baseline suite; images add extras with TEST_SUITES:append
TEST_SUITES = "tegra_identity tegra_versions"

inherit nopackages
