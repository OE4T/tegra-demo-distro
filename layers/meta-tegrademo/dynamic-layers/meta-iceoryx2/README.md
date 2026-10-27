# Holoscan SDK for NVIDIA Tegra (Jetson) platforms

This dynamic layer provides `packagegroup-demo-holoscan`, which
`demo-image-holoscan` installs:

| package | contents |
|---|---|
| `packagegroup-demo-holoscan` | the [Holoscan SDK](https://github.com/nvidia-holoscan/holoscan-sdk), its Python bindings and Holoscan Camera |
| `packagegroup-demo-holoscan-tests` | their examples, benchmarks and ptests |

meta-tegra-community only provides the Holoscan recipes when the
[meta-iceoryx2](https://github.com/nvidia-holoscan/meta-iceoryx2) layer
is in the build, so `demo-image-holoscan` is skipped without that layer.

## Build with tegra-demo-distro

Add meta-iceoryx2 to tegra-demo-distro:

```
cd repos
git submodule add -b blacksail https://github.com/nvidia-holoscan/meta-iceoryx2
cd ../layers
ln -s ../repos/meta-iceoryx2
```

Then use the `setup-env` script to start a bitbake shell, and add
the layer to your build:

```
bitbake-layers add-layer ../layers/meta-iceoryx2
```

Finally, build the image using:

```
bitbake demo-image-holoscan
```

## SDK

The standard SDK of the image cross-builds Holoscan applications:

```
bitbake demo-image-holoscan -c populate_sdk
```

Install it from `tmp/deploy/sdk/`, source its `environment-setup-*`
script, and configure an application with CMake against the Holoscan
package in the SDK sysroot. `packagegroup-demo-holoscan-tests` and
Jetson IO are not part of the SDK.
