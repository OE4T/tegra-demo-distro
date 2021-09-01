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

TEGRACHIPID="$(printf "0x%02x" $(cat /sys/module/tegra_fuse/parameters/tegra_chip_id))"
SAMPLEROOT="/opt/nvidia/vpi1"
PATH="$SAMPLEROOT/bin:$PATH"
SAMPLEASSETS="$SAMPLEROOT/assets"
SKIPCODE=97

run_convolve_2d() {
    if [ "$TEGRACHIPID" != "0x19" ] && [ "$1" = "pva" ]; then
        echo "Skipping 01_convolve_2d - pva backend is not supported"
        return $SKIPCODE
    fi
    echo "Running 01_convolve_2d - Backend is $1"
    vpi_sample_01_convolve_2d "$1" "$SAMPLEASSETS/kodim08.png"
}

run_stereo_disparity() {
    if [ "$TEGRACHIPID" != "0x19" ] && [ "$1" = "pva" ]; then
        echo "Skipping 02_stereo_disparity - pva backend is not supported"
        return $SKIPCODE
    fi
    echo "Running 02_stereo_disparity - Backend is $1"
    vpi_sample_02_stereo_disparity "$1" "$SAMPLEASSETS/chair_stereo_left.png" "$SAMPLEASSETS/chair_stereo_right.png"  
}

run_harris_corners() {
    if [ "$TEGRACHIPID" != "0x19" ] && [ "$1" = "pva" ]; then
        echo "Skipping 03_harris_corners - pva backend is not supported"
        return $SKIPCODE
    fi
    echo "Running 03_harris_corners - Backend is $1"
    vpi_sample_03_harris_corners "$1" "$SAMPLEASSETS/kodim08.png"
}

run_rescale() {
    if [ "$TEGRACHIPID" != "0x19" ] && [ "$1" = "pva" ]; then
        echo "Skipping 04_rescale - pva backend is not supported"
        return $SKIPCODE
    fi
    echo "Running 04_rescale - Backend is $1"
    vpi_sample_04_rescale "$1" "$SAMPLEASSETS/kodim08.png"
}

run_benchmark() {
    if [ "$TEGRACHIPID" != "0x19" ] && [ "$1" = "pva" ]; then
        echo "Skipping 05_benchmark - pva backend is not supported"
        return $SKIPCODE
    fi
    echo "Running 05_benchmark - Backend is $1"
    vpi_sample_05_benchmark "$1"
}

run_klt_tracker() {
    if [ ! -x "$SAMPLEROOT/bin/vpi_sample_06_klt_tracker" ]; then
        echo "Skipping 06_klt_tracker"
        return $SKIPCODE
    fi
    if [ "$TEGRACHIPID" != "0x19" ] && [ "$1" = "pva" ]; then
        echo "Skipping 06_klt_tracker - pva backend is not supported"
        return $SKIPCODE
    fi
    echo "Running 06_klt_tracker - Backend is $1"
    vpi_sample_06_klt_tracker "$1" "$SAMPLEASSETS/dashcam.mp4" "$SAMPLEASSETS/dashcam_bboxes.txt"
}

run_fft() {
    echo "Running 07_fft - Backend is $1"
    vpi_sample_07_fft "$1" "$SAMPLEASSETS/kodim08.png"
 
}

run_tnr() {
    if [ ! -x "$SAMPLEROOT/bin/vpi_sample_09_tnr" ]; then
        echo "Skipping 09_tnr"
        return $SKIPCODE
    fi
    echo "Running 09_tnr - Backend is $1"
    vpi_sample_09_tnr "$1" "$SAMPLEASSETS/noisy.mp4"
}

run_perspwarp() {
    if [ ! -x "$SAMPLEROOT/bin/vpi_sample_10_perspwarp" ]; then
        echo "Skipping 10_perspwarp"
        return $SKIPCODE
    fi
    echo "Running 10_perspwarp - Backend is $1"
    vpi_sample_10_perspwarp "$1" "$SAMPLEASSETS/noisy.mp4"
}

run_fisheye() {
    echo "Running 11_fisheye"
    vpi_sample_11_fisheye -c 10,7 -s 22 "$SAMPLEASSETS/fisheye/"*.jpg
}

run_optflow_lk() {
    if [ ! -x "$SAMPLEROOT/bin/vpi_sample_12_optflow_lk" ]; then
        echo "Skipping 12_optflow_lk"
        return $SKIPCODE
    fi
    echo "Running 12_optflow_lk - Backend is $1"
    vpi_sample_12_optflow_lk "$1" "$SAMPLEASSETS/dashcam.mp4" 5 frame.png
}

run_optflow_dense() {
    if [ ! -x "$SAMPLEROOT/bin/vpi_sample_13_optflow_dense" ]; then
        echo "Skipping 13_optflow_dense"
        return $SKIPCODE
    fi
    echo "Running 13_optflow_dense"
    vpi_sample_13_optflow_dense "$1" "$SAMPLEASSETS/pedestrians.mp4" high
}

run_background_subtractor() {
    if [ ! -x "$SAMPLEROOT/bin/vpi_sample_14_background_subtractor" ]; then
        echo "Skipping 14_background_subtractor"
        return $SKIPCODE
    fi
    echo "Running 14_background_subtractor - Backend is $1"
    vpi_sample_14_background_subtractor "$1" "$SAMPLEASSETS/pedestrians.mp4"
}

# VPI samples list
TESTS="convolve_2d stereo_disparity harris_corners rescale benchmark"
TESTS="$TESTS klt_tracker fft tnr perspwarp fisheye optflow_lk optflow_dense"
TESTS="$TESTS background_subtractor"

# List of VPI backend per sample app
convolve_2d=("cpu" "cuda" "pva")
stereo_disparity=("cpu" "cuda" "pva" "pva-nvenc-vic")
harris_corners=("cpu" "cuda" "pva")
rescale=("cpu" "cuda" "pva")
benchmark=("cpu" "cuda" "pva")
klt_tracker=("cpu" "cuda" "pva")
fft=("cpu" "cuda")
tnr=("cuda" "vic")
perspwarp=("cpu" "cuda" "vic")
fisheye=("cuda")
optflow_lk=("cpu" "cuda")
optflow_dense=("nvenc")
background_subtractor=("cpu" "cuda")

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
        declare -n backendList=$t
        for backend in ${backendList[@]}; do
            testcount=$((testcount+1))
            echo "=== BEGIN: $t ==="
            if run_$t $backend; then
                echo "=== PASS:  $t ==="
                testpass=$((testpass+1))
            elif [ $? -eq $SKIPCODE ]; then
                echo "=== SKIP:  $t ==="
                testskip=$((testskip+1))
                break
            else
                echo "=== FAIL:  $t ==="
                testfail=$((testfail+1))
            fi
        done
    fi
done

echo "Tests run:     $testcount"
echo "Tests passed:  $testpass"
echo "Tests skipped: $testskip"
echo "Tests failed:  $testfail"
exit $testfail
