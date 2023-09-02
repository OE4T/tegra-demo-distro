# tegra-demo-distro

Reference/demo distribution for NVIDIA Jetson platforms
using Yocto Project tools and the [meta-tegra](https://github.com/OE4T/meta-tegra) BSP layer.

![Build status](https://builder.madison.systems/badges/tegrademo-kirkstone.svg)

Metadata layers are brought in as git submodules:

| Layer Repo            | Branch         | Description                                         |
| --------------------- | ---------------|---------------------------------------------------- |
| poky                  | kirkstone      | OE-Core from poky repo at yoctoproject.org          |
| meta-tegra            | kirkstone      | L4T BSP layer - L4T R35.4.1/JetPack 5.1.2           |
| meta-tegra-community  | kirkstone      | OE4T layer with additions from the community        |
| meta-openembedded     | kirkstone      | OpenEmbedded layers                                 |
| meta-virtualization   | kirkstone      | Virtualization layer for docker support             |

## Prerequisites

See the [Yocto Project Quick Build](https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html)
documentation for information on setting up your build host.

For burning SDcards (for Jetson Xavier NX developer kits), the `bmap-tools`
package is recommended.

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

# Contributing

Please see the contributor wiki page at [this link](https://github.com/OE4T/meta-tegra/wiki/OE4T-Contributor-Guide).
Contributions are welcome!
