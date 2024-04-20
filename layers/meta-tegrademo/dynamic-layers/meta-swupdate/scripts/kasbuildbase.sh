#!/bin/bash
base=$(basename $0 .sh)
machine=$(echo $base | cut -s -d '-' -f 2-)
if [ ! -z "${machine}" ]; then
    echo "building for machine ${machine}"
    export KAS_MACHINE=${machine}
fi
base_layer_path=$(realpath $(dirname $0))/../
echo "move to the base repo directory"
pushd $(dirname $0)/../../../../../
echo "Ensure we've setup submodules at least once"
git submodule update --init --recursive
kas build --update ${base_layer_path}/conf/kas/swupdate-oe4t.yml
