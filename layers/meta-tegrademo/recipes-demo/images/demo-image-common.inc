IMAGE_FEATURES += "ssh-server-openssh"

LICENSE = "MIT"

inherit core-image

CORE_IMAGE_BASE_INSTALL += "packagegroup-demo-base packagegroup-demo-basetests"
CORE_IMAGE_BASE_INSTALL += "${@'packagegroup-demo-systemd' if d.getVar('VIRTUAL-RUNTIME_init_manager') == 'systemd' else ''}"

inherit nopackages
