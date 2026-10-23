DESCRIPTION = "Additional reference test tools for Tegra QA validation"

LICENSE = "MIT"

inherit packagegroup

RDEPENDS:${PN} = " \
    bpftool \
    iperf3 \
    tcpdump \
    xdp-tools \
    lmbench \
    perf \
    rt-tests \
    stress-ng \
    v4l-utils \
    glmark2 \
    kmscube \
    tegra-vulkan-sc-samples \
    tegra-libraries-camera-nvraw \
    nvgstipctestapp \
    gstreamer1.0-plugins-base-opus \
    gstreamer1.0-libav \
    gstreamer1.0-plugins-ugly-x264 \
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
