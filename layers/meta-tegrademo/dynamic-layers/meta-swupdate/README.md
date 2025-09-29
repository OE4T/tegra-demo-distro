# Swupdate for NVIDIA Tegra (Jetson) platforms

This dynamic layer provides an example implementation for
Nvidia Jetson and [swupdate](https://sbabic.github.io/swupdate).

The simplest way to use on tegra is to add to a forked copy of
[tegra-demo-distro](https://github.com/OE4T/tegra-demo-distro) which
also contains relevant images and submodules used to build tegra images.
However, this is not strictly required.  The only dependency required
is the [meta-tegra](https://github.com/OE4T/meta-tegra) layer.

## Build with tegra-demo-distro

Use these instructions to add to tegra-demo-distro on whatever
branch you'd like to target (kirkstone and later are supported).

```
cd repos
git submodule add https://github.com/sbabic/meta-swupdate
cd ../layers
ln -s ../repos/meta-swupdate
```

Then use the `setup-env` script to start a bitbake shell, and add
this layer to your build
```
bitbake-layers add-layer ../layers/meta-swupdate
```

In your local.conf (or distro/machine configuration) add
these lines:
```
IMAGE_INSTALL:append = " swupdate"
USE_REDUNDANT_FLASH_LAYOUT = "1"
IMAGE_FSTYPES:append = " tar.gz"
```
If you desire an image other than demo-image-base as your base image,
you may add a definition for `SWUPDATE_CORE_IMAGE_NAME` with the
desired base image.

Finally, build the update image using:
```
bitbake swupdate-image-tegra
```

## Deploy and Test
* Tegraflash the inital image (demo-image-base or, whatever
image you've set as `SWUPDATE_CORE_IMAGE_NAME`
* Deploy the .swu file built with swupdate-image-tegra
to the target
* Run the update with:
```
swupdate -i </path/to/swu/file>
```
* Reboot to apply the update.
  * The root partition should change
  * The `nvbootctrl dump-slots-info` output should show boot
from the alternate boot slot with `Capsule update status:1`.

# Build Options

The tegra_swupdate.bbclass contains global configuration options
for the swupdate demo.

## TEGRA_SWUPDATE_BOOTLOADER_INSTALL_ONLY_IF_DIFFERENT

Set
```
TEGRA_SWUPDATE_BOOTLOADER_INSTALL_ONLY_IF_DIFFERENT = "true"
```
in your local.conf or layer to only run the capsule update when
a different bootloader version is detected in the alternate slot,
where bootloader version is set based on ${L4T_VERSION} but can
be modified by overriding variable `TEGRA_SWUPDATE_BOOTLOADER_VERSION`

When this variable is set, the capsule payload will not be installed
as a part of the update when the alternate partition is found to contain
the same bootloader release version (rootfs was built with the same
value of `TEGRA_SWUPDATE_BOOTLOADER_VERSION`.  Instead, the rootfs
will be switched to the alternate rootfs.
