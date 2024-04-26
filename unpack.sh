#!/bin/bash
image=ds-image-sato
#image=demo-image-sato
#machine=jetson-orin-nx-devkit
machine=jetson-orin-nx-a603
builddir=build

scriptdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
deployfile=$(realpath ${scriptdir}/${builddir}/tmp/deploy/images/${machine}/${image}-${machine}.tegraflash.tar.gz)
 
#tmpdir=`mktemp`
tmpdir=/tmp/ds-flash-${machine}

rm -rf $tmpdir
mkdir -p $tmpdir
echo "Using temp directory $tmpdir"
pushd "$tmpdir"
cp $deployfile .
tar -xvf $deployfile
set -e
