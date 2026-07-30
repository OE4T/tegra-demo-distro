DESCRIPTION = "Additional reference test tools for Tegra QA validation"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    iperf3 \
    lmbench \
    perf \
    rt-tests \
    stress-ng \
    kernel-module-uvcvideo \
    v4l-utils \
    glmark2 \
    kmscube \
    tegra-vulkan-sc-samples \
    tegra-libraries-camera-nvraw \
    nvgstipctestapp \
    gstreamer1.0-plugins-base-opus \
    gstreamer1.0-libav \
    python3-jetson-io \
    fio \
    yavta \
    dhrystone \
    schbench \
    stream \
    python3-pytest \
    sysbench \
    cpuburn-arm \
    stressapptest \
    memtester \
    tinymembench \
    iozone3 \
    cpupower \
"
