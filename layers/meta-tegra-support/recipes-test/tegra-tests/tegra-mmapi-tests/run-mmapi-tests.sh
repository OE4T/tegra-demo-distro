#!/bin/sh
# SPDX-License-Identifier: MIT
# Copyright (c) 2021, OpenEmbedded for Tegra Project
#
# WARNING: make sure you have at least a couple of GiB of free
# space availabe in the current working directory, as some of
# these samples generate very large files.
#
# Some of these tests work better if you use jetson_clocks to
# speed things up.

SAMPLEROOT="/opt/tegra-mmapi"
PATH="$SAMPLEROOT/bin:$PATH"
SAMPLEVID="$SAMPLEROOT/data/Video/sample_outdoor_car_1080p_10fps.h264"
SAMPLEYUV="samplevid.yuv"
SAMPLEJPG="$SAMPLEROOT/data/Picture/nvidia-logo.jpg"
SAMPLEYUVPIC="nvidia-logo.yuv"
SAMPLEMODELS="$SAMPLEROOT/data/Model"
SKIPCODE=97

run_video_decode() {
    vid="${1:-$SAMPLEVID}"
    echo "Running 00_video_decode on $vid"
    video_decode H264 "$vid"
}

generate_yuv_sample_vid() {
    echo "Converting sample video to YUV, please wait"
    video_dec_cuda "$SAMPLEVID" H264 --disable-rendering -o "$SAMPLEYUV" -f 2
}

run_video_encode() {
    local rc=0
    [ -e "$SAMPLEYUV" ] || generate_yuv_sample_vid
    echo "Running 01_video_encode"
    rm -f samplevid.h264
    video_encode "$SAMPLEYUV" 1920 1080 H264 samplevid.h264 || rc=1
    [ $rc -ne 0 ] || run_video_decode samplevid.h264 || rc=1
    rm -f samplevid.h264
    return $rc
}

run_video_dec_cuda() {
    vid="${1:-$SAMPLEVID}"
    echo "Running 02_video_dec_cuda $vid"
    if [ -n "$2" ]; then
	video_dec_cuda "$vid" H264 --bbox-file "$2"
    else
	video_dec_cuda "$vid" H264
    fi
}

run_video_enc_cuda() {
    local rc=0
    [ -e "$SAMPLEYUV" ] || generate_yuv_sample_vid
    echo "Running 03_video_cuda_enc"
    rm -f samplevid.h264
    video_cuda_enc "$SAMPLEYUV" 1920 1080 H264 samplevid.h264 || rc=1
    [ $rc -ne 0 ] || run_video_dec_cuda samplevid.h264 || rc=1
    rm -f samplevid.h264
    return $rc
}

run_video_dec_trt() {
    if [ ! -x "$SAMPLEROOT/bin/video_dec_trt" ]; then
	echo "Skipping 04_video_dec_trt"
	return $SKIPCODE
    fi
    local rc=0
    echo "Running 04_video_dec_trt"
    video_dec_trt 2 "$SAMPLEVID" "$SAMPLEVID" H264 --trt-onnxmodel "$SAMPLEROOT/data/Model/resnet10/resnet10_dynamic_batch.onnx" --trt-mode 0 || rc=1
    [ $rc -ne 0 ] || run_video_dec_cuda "$SAMPLEVID" "result0.txt" || rc=1
    [ $rc -ne 0 ] || run_video_dec_cuda "$SAMPLEVID" "result1.txt" || rc=1
    rm -f result0.txt result1.txt trtModel.cache
    return $rc
}

run_jpeg_encode() {
    local rc=0
    [ -e "$SAMPLEYUVPIC" ] || run_jpeg_decode
    echo "Running 05_jpeg_encode"
    jpeg_encode "$SAMPLEYUVPIC" 1920 1080 "sample-encoded.jpg" || rc=1
    rm -f sample-encoded.jpg
    return $rc
}

run_jpeg_decode() {
    jpeg="${1:-$SAMPLEJPG}"
    yuv="${2:-$SAMPLEYUVPIC}"
    echo "Running 06_jpeg_decode"
    jpeg_decode num_files 1 "$jpeg" "$yuv"
}

run_video_convert() {
    local rc=0
    [ -e "$SAMPLEYUVPIC" ] || run_jpeg_decode
    video_convert "$SAMPLEYUVPIC" 1920 1080 YUV420 sample.yuyv 1920 1080 YUYV || rc=1
    rm -f sample.yuyv
    return $rc
}

run_video_dec_drm() {
    if [ -n "$DISPLAY" ]; then
	echo "Cannot run 08_video_dec_drm when running from X, skipping"
	return $SKIPCODE
    fi
    local rc=0
    for i in 0 1 2; do
	if [ -e /sys/class/graphics/fb${i} ]; then
	    echo "4" > /sys/class/graphics/fb${i}/blank
	    echo "0x0" > /sys/class/graphics/fb${i}/device/win_mask
	fi
    done
    echo "0x3f" > /sys/class/graphics/fb0/device/win_mask
    echo "0" > /sys/class/graphics/fb0/blank
    xstatus=$(systemctl is-active xserver-nodm)
    if [ "$xstatus" = "active" ]; then
	systemctl stop xserver-nodm
    fi
    echo "Running 08_video_dec_drm"
    video_dec_drm "$SAMPLEVID" H264 || rc=1
    if [ "$xstatus" = "active" ]; then
	systemctl start xserver-nodm
    fi
    return $rc
}

run_camera_jpeg_capture() {
    local mipicam=$(find_argus_camera)
    if [ -z "$mipicam" ]; then
	echo "Skipping 09_camera_jpeg_capture - no MIPI camera"
	return $SKIPCODE
    fi
    local rc=0
    echo "Running 09_camera_jpeg_capture"
    camera_jpeg_capture || rc=1
    rm -f output*.jpg
    return $rc
}

run_camera_recording() {
    local mipicam=$(find_argus_camera)
    if [ -z "$mipicam" ]; then
	echo "Skipping 10_camera_recording - no MIPI camera"
	return $SKIPCODE
    fi
    local rc=0
    echo "Running 10_camera_recording"
    camera_recording || rc=1
    [ $rc -ne 0 ] || run_video_decode output.h264 || rc=1
    rm -f output.h264
    return $rc
}

find_usb_camera() {
    for d in /dev/video*; do
	[ -c "$d" ] || continue
	if readlink -f /sys/class/video4linux/$(basename $d) | grep -q usb; then
	    echo "$d"
	    return
	fi
    done
    echo ""
}

find_argus_camera() {
    for d in /dev/video*; do
	[ -c "$d" ] || continue
	if readlink -f /sys/class/video4linux/$(basename $d) | grep -q host1x; then
	    echo "$d"
	    return
	fi
    done
    echo ""
}

run_camera_v4l2_cuda() {
    local usbcam=$(find_usb_camera)
    if [ -z "$usbcam" ]; then
	echo "Skipping 12_camera_v4l2_cuda - no USB camera"
	return $SKIPCODE
    fi
    echo "Running 12_camera_v4l2_cuda -d $usbcam"
    camera_v4l2_cuda -d $usbcam -s 1280x720 -f YUYV -c -N 120
}

run_camera_sample() {
    local mipicam=$(find_argus_camera)
    if [ -z "$mipicam" ]; then
	echo "Skipping camera_unit_sample - no MIPI camera"
	return $SKIPCODE
    fi
    camera_sample -sid ${mipicam##/dev/video}
}

run_decode_sample() {
    local rc=0
    echo "Running decode_sample"
    decode_sample "$SAMPLEVID" ut-samplevid.yuv || rc=1
    rm -f ut-samplevid.yuv
    return $rc
}

run_encode_sample() {
    local rc=0
    [ -e "$SAMPLEYUV" ] || generate_yuv_sample_vid
    echo "Running encode_sample"
    rm -f ut-samplevid.h264
    encode_sample "$SAMPLEYUV" 1920 1080 ut-samplevid.h264 || rc=1
    [ $rc -ne 0 ] || run_video_decode ut-samplevid.h264 || rc=1
    rm -f ut-samplevid.h264
    return $rc
}

run_transform_sample() {
    local rc=0
    [ -e "$SAMPLEYUV" ] || generate_yuv_sample_vid
    echo "Running transform_sample"
    transform_sample "$SAMPLEYUV" yuv420 1920 1080 nv12-sample.yuv nv12 || rc=1
    rm -f nv12-sample.yuv
    return $rc
}

run_backend() {
    if [ ! -x "$SAMPLEROOT/bin/backend" ]; then
	echo "Skipping backend"
	return $SKIPCODE
    fi
    mbase="$SAMPLEMODELS/GoogleNet_one_class/GoogleNet_modified_oneClass_halfHD"
    echo "Running backend"
    backend 1 "$SAMPLEVID" H264 --trt-deployfile "${mbase}.prototxt" --trt-modelfile "${mbase}.caffemodel" \
        --trt-mode 0 --trt-proc-interval 1 -fps 10
    rm -f trtModel.cache
}

run_frontend() {
    if [ ! -x "$SAMPLEROOT/bin/frontend" ]; then
	echo "Skipping frontend"
	return $SKIPCODE
    fi
    local mipicam=$(find_argus_camera)
    if [ -z "$mipicam" ]; then
	echo "Skipping frontend - no camera"
	return $SKIPCODE
    fi
    echo "Running frontend"
    mbase="$SAMPLEMODELS/GoogleNet_three_class/GoogleNet_modified_threeClass_VGA"
    frontend --deploy "${mbase}.prototxt" --model "${mbase}.caffemodel" --no-preview -t 10
    rm -f output*.h265 trt.h264 trtModel.cache
}

run_v4l2cuda() {
    local usbcam=$(find_usb_camera)
    if [ -z "$usbcam" ]; then
	echo "Skipping run_v4l2cuda - no USB camera"
	return $SKIPCODE
    fi
    echo "Running capture-cuda -d $usbcam"
    capture-cuda -d $usbcam
    rm -f out.ppm
}

TESTS="video_decode video_encode video_dec_cuda video_enc_cuda video_dec_trt jpeg_encode"
TESTS="$TESTS jpeg_decode video_convert video_dec_drm camera_jpeg_capture camera_recording"
TESTS="$TESTS camera_v4l2_cuda camera_sample decode_sample encode_sample transform_sample"
TESTS="$TESTS backend frontend v4l2cuda"

find_test() {
    for t in $TESTS; do
	if [ "$t" = "$1" ]; then
	    echo "$t"
	    return
	fi
    done
}

jetson_clocks

testcount=0
testpass=0
testfail=0
testskip=0
if [ $# -eq 0 ]; then
    tests_to_run="$TESTS"
else
    tests_to_run="$@"
fi

for cand in $tests_to_run; do
    t=$(find_test "$cand")
    if [ -z "$t" ]; then
	echo "ERR: unknown test: $cand" >&2
    else
	testcount=$((testcount+1))
	echo "=== BEGIN: $t ==="
	if run_$t; then
	    echo "=== PASS:  $t ==="
	    testpass=$((testpass+1))
	elif [ $? -eq $SKIPCODE ]; then
	    echo "=== SKIP:  $t ==="
	    testskip=$((testskip+1))
	else
	    echo "=== FAIL:  $t ==="
	    testfail=$((testfail+1))
	fi
    fi
done

echo "Tests run:     $testcount"
echo "Tests passed:  $testpass"
echo "Tests skipped: $testskip"
echo "Tests failed:  $testfail"
exit $testfail
