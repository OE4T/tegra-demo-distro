#!/bin/bash

# Run this script prior to flashing a sensor
# This script will take as input the hostname for the sensor
# and assumes that the ssh pubkey and the tailscale auth key (and eventually the 
# wireguard secret and some other configs) are located in the "secrets" directory
#


image=ds-image-sato
machine=jetson-xavier-nx-devkit
builddir=build

set -e

function usage {
  echo "Usage: $0 -n <hostname>"
  echo "  [-i <image>]      The image to flash (default: ds-image-sato)"
  echo "  [-m <machine>]    The machine to flash (default: jetson-xavier-nx-devkit-emmc)"
  exit 1
}

while getopts "i:m:n:" opt; do
  case ${opt} in
    i )
      image=$OPTARG
      ;;
    m )
      machine=$OPTARG
      ;;
    n )
      hostname=$OPTARG
      ;;
    \? )
      usage
      ;;
  esac
done


# get current directory 
curdir=$(pwd)

# Make sure the user is root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Check that the appropriate directory in /tmp exists
if [ ! -d /tmp/ds-flash-${machine} ]; then
  echo "The directory /tmp/ds-flash-jetson-xavier-nx-devkit-emmc does not exist"
  exit
fi


# Check that the sparse image (*.ext4.img) doesn't exist; delete it if it does
echo "Checking for existing sparse image..."
if [ -f /tmp/ds-flash-${machine}/${image}.ext4.img ]; then
  echo "The file /tmp/ds-flash-${machine}/${image}.ext4.img already exists"
  echo "Deleting old sparse image..."
  rm /tmp/ds-flash-jetson-xavier-nx-devkit-emmc/${image}.ext4.img
  echo "Old sparse image deleted"
fi

# create a mount point for the image 
echo "Checking for mount point..."
if [ ! -d ${curdir}/rootfs-${machine}/mnt ]; then
  mkdir -p ${curdir}/rootfs-${machine}/mnt
fi

# mount the image
echo "Mounting the image..."
mount -o loop /tmp/ds-flash-${machine}/${image}.ext4 ${curdir}/rootfs-${machine}/mnt

# edit the host name in the image (/etc/hostname)
echo "Editing the hostname in the image..."
echo "Setting the hostname to ${hostname}"
echo ${hostname} > ${curdir}/rootfs-${machine}/mnt/etc/hostname

# TODO Check that the secrets directory exists
if [ -d ${curdir}/secrets ]; then
    if [ -f ${curdir}/secrets/sensor_id_ed25519.pub ]; then
        echo "Copying the ssh pubkey to the image..."
        mkdir -p ${curdir}/rootfs-${machine}/mnt/home/ds/.ssh
        cp ${curdir}/secrets/sensor_id_ed25519.pub ${curdir}/rootfs-${machine}/mnt/home/ds/.ssh/authorized_keys
        # make sure the pubkey has the appropriate permissions
        chmod 600 ${curdir}/rootfs-${machine}/mnt/home/ds/.ssh/authorized_keys
        chmod 700 ${curdir}/rootfs-${machine}/mnt/home/ds/.ssh
        chown -R 1200:1200 ${curdir}/rootfs-${machine}/mnt/home/ds/.ssh
    else
        echo "The ssh pubkey does not exist"
        exit
    fi
else
  echo "The secrets directory does not exist"
  exit
fi

# Disable password ssh 
echo "Disabling password ssh..."
sudo sed -i -e '/^PasswordAuthentication[[:space:]]/s/^/#/' -e '$aPasswordAuthentication no' ${curdir}/rootfs-${machine}/mnt/etc/ssh/sshd_config


# copy the tailscale auth key to the image

# add the /data mount point
echo "Ensuring /data directory exists..."
if [ ! -d ${curdir}/rootfs-${machine}/mnt/data ]; then
    mkdir ${curdir}/rootfs-${machine}/mnt/data
    echo "/data directory created."
else
    echo "/data directory already exists."
fi

# mount the ssd 
echo "Adding fstab entry for /dev/nvme0n1..."
FSTAB_ENTRY="/dev/nvme0n1 /data ext4 defaults 0 2"

# First, ensure the entry does not already exist to avoid duplicates
if ! grep -q "/dev/nvme0n1" ${curdir}/rootfs-${machine}/mnt/etc/fstab; then
    echo "$FSTAB_ENTRY" >> ${curdir}/rootfs-${machine}/mnt/etc/fstab
    echo "fstab entry added."
else
    echo "fstab entry for /dev/nvme0n1 already exists."
fi

# unmount the fs image
echo "Unmounting the image..."
umount ${curdir}/rootfs-${machine}/mnt
