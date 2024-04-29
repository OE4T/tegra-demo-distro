#!/bin/bash
#

if [ $# -ne 2 ]; then
    echo "Usage: $0 <machine> <distro>"
    exit 1
fi

MACHINE=$1
DISTRO=$2
shift 2

# Set up the environment
source /yocto/setup-env --machine $MACHINE --distro $DISTRO

exec /bin/bash
