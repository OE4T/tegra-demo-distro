# tegra-demo-distro

Reference/demo distribution for NVIDIA Jetson platforms
using Yocto Project tools and the [meta-tegra](https://github.com/OE4T/meta-tegra) BSP layer.

![Build status](https://builder.madison.systems/badges/tegrademo-scarthgap.svg)

Metadata layers are brought in as git submodules:

| Layer Repo            | Branch         | Description                                         |
| --------------------- | ---------------|---------------------------------------------------- |
| poky                  | scarthgap      | OE-Core from poky repo at yoctoproject.org          |
| meta-tegra            | scarthgap      | L4T BSP layer - L4T R36.4.0/JetPack 6.1             |
| meta-tegra-community  | scarthgap      | OE4T layer with additions from the community        |
| meta-openembedded     | scarthgap      | OpenEmbedded layers                                 |
| meta-virtualization   | scarthgap      | Virtualization layer for docker support             |

## Prerequisites

See the [Yocto Project Quick Build](https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html)
documentation for information on setting up your build host.

## Setting up

1. Clone this repository:

        $ git clone https://github.com/OE4T/tegra-demo-distro.git

2. Switch to the appropriate branch, using the
   [wiki page](https://github.com/OE4T/tegra-demo-distro/wiki/Which-branch-should-I-use%3F)
   for guidance.

3. Initialize the git submodules:

        $ cd tegra-demo-distro
        $ git submodule update --init

4. Source the `setup-env` script to create a build directory,
   specifying the MACHINE you want to configure as the default
   for your builds. For example, to set up a build directory
   called `build` that is set up for the Jetson Xavier NX
   developer kit and the default `tegrademo` distro:

        $ . ./setup-env --machine jetson-xavier-nx-devkit

   You can get a complete list of available options, MACHINE
   names, and DISTRO names with

        $ . ./setup-env --help

5. Optional: Install pre-commit hook for commit autosigning using
        $ ./scripts-setup/setup-git-hooks

## Distributions

Use the `--distro` option with `setup-env` to specify a distribution for your build,
or customize the DISTRO setting in your `$BUILDDIR/conf/local.conf` to reference one
of the supported distributions.

Currently supported distributions are listed below:


| Distribution name | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| tegrademo         | Default distro used to demonstrate/test meta-tegra features   |

## Images

The `tegrademo` distro includes the following image recipes, which
are dervied from the `core-image-XXX` recipes in OE-Core but configured
for Jetson platforms. They include some additional test tools and
demo applications.

| Recipe name       | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| demo-image-base   | Basic image with no graphics                                  |
| demo-image-egl    | Base with DRM/EGL graphics, no window manager                 |
| demo-image-sato   | X11 image with Sato UI                                        |
| demo-image-weston | Wayland with Weston compositor                                |
| demo-image-full   | Sato image plus nvidia-docker, openCV, multimedia API samples |

### Update image demo

A [swupdate](https://sbabic.github.io/swupdate/) demo image is also available which supports
A/B rootfs updates to any of the supported images.  For details refer to
[layers/meta-tegrademo/dynamic-layers/meta-swupdate/README.md](layers/meta-tegrademo/dynamic-layers/meta-swupdate/README.md).

# Contributing

Please see the contributor wiki page at [this link](https://github.com/OE4T/meta-tegra/wiki/OE4T-Contributor-Guide).
Contributions are welcome!
