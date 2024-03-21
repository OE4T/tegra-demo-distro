#!/bin/bash
#image=core-image-sato-dev
#machine=jetson-xavier-nx-devkit
#suffix=20231128211311

#deployfile=${image}-${machine}-${suffix}.tegraflash.tar.gz

scriptdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
 
echo "script dir: $scriptdir"
deployfile=ds-image-sato-jetson-xavier-nx-devkit-20240131192152.tegraflash.tar.gz
#deployfile=demo-image-weston-jetson-xavier-nx-devkit-20240110150946.tegraflash.tar.gz
tmpdir=`mktemp`

rm -rf $tmpdir
mkdir -p $tmpdir
echo "Using temp directory $tmpdir"
pushd "$tmpdir"
cp $scriptdir/$deployfile .
tar -xvf $deployfile
set -e
