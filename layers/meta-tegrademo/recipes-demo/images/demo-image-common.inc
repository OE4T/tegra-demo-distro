IMAGE_FEATURES += "ssh-server-openssh"

LICENSE = "MIT"

inherit core-image

CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-base packagegroup-demo-basetests"
CORE_IMAGE_BASE_INSTALL += "${@'packagegroup-demo-systemd' if d.getVar('VIRTUAL-RUNTIME_init_manager') == 'systemd' else ''}"
CORE_IMAGE_BASE_INSTALL += "nv-tegra-release"
TOOLCHAIN_HOST_TASK += "nativesdk-packagegroup-cuda-sdk-host"

# baseline suite; images add their extras via TEST_SUITES:append (not the "auto" set)
TEST_SUITES = "ping ssh date df oe_syslog \
               tegra_identity tegra_versions tegra_storage tegra_thermal \
               tegra_boottime tegra_console tegra_usb tegra_network \
               tegra_watchdog tegra_esrt tegra_partition tegra_nvpmodel \
               tegra_kmodule tegra_nvbootctrl tegra_overlay tegra_optee \
               tegra_samples tegra_display tegra_reboot tegra_suspend"

inherit nopackages
