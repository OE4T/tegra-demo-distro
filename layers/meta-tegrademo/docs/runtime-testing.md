# Tegra runtime testing

meta-tegrademo ships an oeqa runtime test suite for Jetson/Tegra images. It is a
set of `tegra_*` test cases plus the enablement to run them either off the build
host (testexport) or on it (testimage). The suite mirrors OE4T's NVIDIA L4T release
validation matrix and assumes no particular board, carrier, or recovery harness.

## What is here

```
lib/oeqa/runtime/cases/tegra_*.py        the test cases
lib/oeqa/runtime/cases/parselogs-ignores-tegra.txt   dmesg-noise allowlist for parselogs
lib/oeqa/controllers/tegratarget.py      optional testimage controller (flash + power)
conf/tegra-testexport.conf               enable off-host testing (require it)
conf/tegra-testimage.conf                enable on-host testing (require it)
conf/jetpack-{6.2,7.2}.env               per-release version floors
```

The bench is assumed fully wired: RJ45, USB storage, a DisplayPort monitor, and
cameras all attached. A test runs on the images that ship the feature it exercises
(see the table below) and fails loudly when that feature is present but broken.
Hardware that is attached but not working (a driver that fails to bind, a monitor
that returns no EDID) is a failure, never a skip and never a pass. A case skips
only when its peripheral is genuinely absent, when the transport is serial-only
(the reboot, deep-sleep, and swupdate cycles need SSH to reconnect), or when its
content is package-gated and not installed.

## Two ways to run

`testexport` and `testimage` run the same `TEST_SUITES`; they differ in where and
when the tests execute.

- **testexport (off-host).** `bitbake <image> -c testexport` builds a
  self-contained bundle that `oe-test` runs later, elsewhere, with no build tree.
  It supports the `serial` target (a console-only DUT with no network) and the
  `simpleremote` target (SSH). This is the path for a laptop or a flashing rig
  that is separate from the build farm, and for running one bundle across many
  boards. No controller is involved.
- **testimage (on-host).** `bitbake <image> -c testimage` runs the suite on the
  build host immediately after the build, against a running board reached over
  SSH. Use it for CI gating. The `TegraTarget` controller can additionally flash
  and power-cycle the board first (see below).

Enable either (or both) by requiring the matching fragment in the build's
`conf/local.conf`:

```
require conf/tegra-testexport.conf
require conf/tegra-testimage.conf
```

## Per-image suites

Each demo image runs the baseline from `demo-image-common.inc` plus the extras
its components need, appended in the image recipe.

| Image | Adds over the baseline |
| --- | --- |
| demo-image-egl | `tegra_gstreamer`, `tegra_camera` |
| demo-image-sato, demo-image-weston | the above plus `tegra_vulkan` |
| demo-image-full | the above plus `tegra_vpi`, `tegra_mmapi`, `tegra_opencv`, `tegra_tensorrt`, `tegra_capsule`, `tegra_docker`, and `tegra_deepstream` (docker arrives via the meta-virtualization bbappend; the gated suites self-skip until their content is installed) |

The swupdate kas fragment adds `tegra_swupdate` on the redundant-layout image.

### Optional test packages

Some validation rows need content the demo images do not carry by default, either
because it is large (DeepStream, the L4T ML containers) or build-option gated (the
OpenCV CUDA modules). Install the package in the image under test and the matching
case runs; leave it out and the case skips. Add them in `local.conf`:

| Add to the image | Enables |
| --- | --- |
| the `libopencv-cuda*` modules | `tegra_opencv` |
| `deepstream-tests` | `tegra_deepstream` |
| `nvidia-docker-tests` | `tegra_docker` (the GPU-container test) |
| `docker nvidia-container-toolkit` (with `meta-virtualization`) | `tegra_docker` |

```
IMAGE_INSTALL:append = " deepstream-tests nvidia-docker-tests \
    libopencv-cudaarithm libopencv-cudabgsegm libopencv-cudacodec \
    libopencv-cudafeatures2d libopencv-cudafilters libopencv-cudaimgproc \
    libopencv-cudalegacy libopencv-cudaobjdetect libopencv-cudaoptflow \
    libopencv-cudastereo libopencv-cudawarping"
```

`tegra_docker` needs the docker engine and the nvidia container runtime; on
`demo-image-full` those come from the
`dynamic-layers/meta-virtualization/recipes-demo/images/demo-image-full.bbappend`.
`tegra_docker`'s GPU-container test adds `nvidia-docker-tests`, whose `run-docker-tests`
runs a GPU workload in the CUDA, PyTorch and TensorFlow NGC containers. It fails hard when
the board cannot reach `nvcr.io`.

`core-image-minimal` is not owned by this layer; set its suite in `local.conf` to
run the peripheral-free baseline.

```
TEST_SUITES:pn-core-image-minimal = "tegra_identity tegra_versions tegra_storage \
    tegra_thermal tegra_boottime tegra_console tegra_usb tegra_network \
    tegra_watchdog tegra_esrt tegra_partition tegra_nvpmodel tegra_kmodule \
    tegra_nvbootctrl tegra_overlay tegra_display tegra_reboot tegra_suspend"
```

The baseline `TEST_SUITES` leads with a small, relevant slice of oe-core cases
(`ping ssh date df oe_syslog`) instead of the full `auto` set, which would pull in
many cases that do not apply to these images (connman, RT, MMC, rtcwake, ...).
`parselogs` is omitted until `parselogs-ignores-tegra.txt` is curated against the
benign L4T driver noise.

### Off-host quick start (serial, no network)

```
# in local.conf:
#   require conf/tegra-testexport.conf
bitbake demo-image-base -c testexport
```

The bundle lands in `tmp/testexport/<image>/` (some configurations place it under
`tmp/testimage/<image>/`). Flash and boot the board by hand (standard
`initrd-flash`), make sure the image offers a root shell on its console, then run
the bundle anywhere with Python and `pexpect`:

```
cd tmp/testexport/demo-image-base
. .../conf/jetpack-7.2.env   # exports the TEGRA_* version floors the tests assert
./oe-test runtime --target-type serial --json-result-dir . \
    */lib/oeqa/runtime/cases
```

The `conf/jetpack-{6.2,7.2}.env` files export the per-release floors
(`TEGRA_L4T_MAJOR/MINOR`, `TEGRA_KERNEL_MIN`, `TEGRA_CUDA_MIN`) that
`tegra_identity` and `tegra_versions` read from the environment; source the one
for the release under test before `oe-test`.

`oe-test` drives the DUT shell through `TEST_SERIALCONTROL_CMD` (a transparent
console bridge such as `picocom -q`, `socat`, or `microcom`, never `minicom`,
whose UI corrupts the stream). Set it for your console device; the value baked
into the bundle is only a placeholder. The oeqa serial target does not log in, so
leave the board at a logged-in root shell, or use an image with serial root
autologin.

For an SSH bundle instead, add the oe-core slice at build time
(`TEST_SUITES:append = " ping ssh date df oe_syslog"`, which `export-parity.sh`
injects) and run with `--target-type simpleremote --target-ip <DUT>`. The reboot,
deep-sleep, capsule, and swupdate cycles reconnect after the board drops, so they
run only on this SSH path and self-skip on serial; SC7 wakes itself via the RTC
(R36.4.3 or newer) and `tegra_swupdate` needs the redundant-layout image.
`tegra_reboot` repeats `TEGRA_REBOOT_CYCLES` times (default 3; the full validation
matrix sets it higher). The board is reached over its RJ45 NIC (or any working
network interface).

### Automated flashing

To make `testimage` flash and power-cycle the board first, set `TEST_TARGET = "TegraTarget"` (`lib/oeqa/controllers/tegratarget.py`). It is hardware-agnostic; recovery, flash, and power run through commands you supply, so any harness works and none is required.

testimage forwards `TEST_POWERCONTROL_CMD` to the controller but not the flash command, so flash settings come from the environment.

```
# in local.conf:
TEST_TARGET = "TegraTarget"
TEST_TARGET_IP = "<dut-ip-or-hostname>"            # the booted DUT, for the test SSH
TEST_POWERCONTROL_CMD = "/path/to/power-control"   # invoked with on|off|cycle

# in the environment, before bitbake <image> -c testimage:
export TEST_FLASHCONTROL_CMD="/path/to/flash-control"   # invoked with the artifact path
export TEST_FLASHCONTROL_ARTIFACT="$DEPLOY_DIR_IMAGE/<image>-<machine>.rootfs.tegraflash-tar.zst"
# export TEST_RCM_BOOT_TIMEOUT=300
```

`start()` flashes (when a flash command is set; otherwise the board is assumed
already flashed), runs `TEST_POWERCONTROL_CMD on`, and waits for the DUT to answer
over SSH; `stop()` runs `TEST_POWERCONTROL_CMD off`. Because the suite runs over
SSH, the DUT must be networked once booted; the no-network case stays on the
off-host serial path. With no harness, oe-core's `dialog-power-control` gives a
manual power prompt.
