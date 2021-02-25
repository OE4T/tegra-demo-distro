inherit kernel-fitimage

FIT_INCLUDE_DTBS ?= "1"
#
# Assemble fitImage
#
# $1 ... .its filename
# $2 ... fitImage name
# $3 ... include ramdisk
fitimage_assemble() {
	kernelcount=1
	dtbcount=""
	DTBS=""
	ramdiskcount=${3}
	setupcount=""
	rm -f ${1} arch/${ARCH}/boot/${2}

	fitimage_emit_fit_header ${1}

	#
	# Step 1: Prepare a kernel image section.
	#
	fitimage_emit_section_maint ${1} imagestart

	uboot_prep_kimage
	fitimage_emit_section_kernel ${1} "${kernelcount}" linux.bin "${linux_comp}"

	#
	# Step 2: Prepare a DTB image section
	#

	if [ "${FIT_INCLUDE_DTBS}" = "1" ]; then
		if [ -z "${EXTERNAL_KERNEL_DEVICETREE}" ] && [ -n "${KERNEL_DEVICETREE}" ]; then
			dtbcount=1
			for DTB in ${KERNEL_DEVICETREE}; do
				if echo ${DTB} | grep -q '/dts/'; then
					bbwarn "${DTB} contains the full path to the the dts file, but only the dtb name should be used."
					DTB=`basename ${DTB} | sed 's,\.dts$,.dtb,g'`
				fi
				DTB_PATH="arch/${ARCH}/boot/dts/${DTB}"
				if [ ! -e "${DTB_PATH}" ]; then
					DTB_PATH="arch/${ARCH}/boot/${DTB}"
				fi

				DTB=$(echo "${DTB}" | tr '/' '_')
				DTBS="${DTBS} ${DTB}"
				fitimage_emit_section_dtb ${1} ${DTB} ${DTB_PATH}
			done
		fi

		if [ -n "${EXTERNAL_KERNEL_DEVICETREE}" ]; then
			dtbcount=1
			for DTB in $(find "${EXTERNAL_KERNEL_DEVICETREE}" \( -name '*.dtb' -o -name '*.dtbo' \) -printf '%P\n' | sort); do
				DTB=$(echo "${DTB}" | tr '/' '_')
				DTBS="${DTBS} ${DTB}"
				fitimage_emit_section_dtb ${1} ${DTB} "${EXTERNAL_KERNEL_DEVICETREE}/${DTB}"
			done
		fi
	fi

	#
	# Step 3: Prepare a setup section. (For x86)
	#
	if [ -e arch/${ARCH}/boot/setup.bin ]; then
		setupcount=1
		fitimage_emit_section_setup ${1} "${setupcount}" arch/${ARCH}/boot/setup.bin
	fi

	#
	# Step 4: Prepare a ramdisk section.
	#
	if [ "x${ramdiskcount}" = "x1" ] ; then
		# Find and use the first initramfs image archive type we find
		for img in cpio.lz4 cpio.lzo cpio.lzma cpio.xz cpio.gz ext2.gz cpio; do
			initramfs_path="${DEPLOY_DIR_IMAGE}/${INITRAMFS_IMAGE_NAME}.${img}"
			echo "Using $initramfs_path"
			if [ -e "${initramfs_path}" ]; then
				fitimage_emit_section_ramdisk ${1} "${ramdiskcount}" "${initramfs_path}"
				break
			fi
		done
	fi

	fitimage_emit_section_maint ${1} sectend

	# Force the first Kernel and DTB in the default config
	kernelcount=1
	if [ -n "${dtbcount}" ]; then
		dtbcount=1
	fi

	#
	# Step 5: Prepare a configurations section
	#
	fitimage_emit_section_maint ${1} confstart

	if [ -n "${DTBS}" ]; then
		i=1
		for DTB in ${DTBS}; do
			dtb_ext=${DTB##*.}
			if [ "${dtb_ext}" = "dtbo" ]; then
				fitimage_emit_section_config ${1} "" "${DTB}" "" "" "`expr ${i} = ${dtbcount}`"
			else
				fitimage_emit_section_config ${1} "${kernelcount}" "${DTB}" "${ramdiskcount}" "${setupcount}" "`expr ${i} = ${dtbcount}`"
			fi
			i=`expr ${i} + 1`
		done
	else
		defaultconfigcount=1
		fitimage_emit_section_config ${1} "${kernelcount}" "" "${ramdiskcount}" "${setupcount}" "${defaultconfigcount}"
	fi

	fitimage_emit_section_maint ${1} sectend

	fitimage_emit_section_maint ${1} fitend

	#
	# Step 6: Assemble the image
	#
	uboot-mkimage \
		${@'-D "${UBOOT_MKIMAGE_DTCOPTS}"' if len('${UBOOT_MKIMAGE_DTCOPTS}') else ''} \
		-f ${1} \
		arch/${ARCH}/boot/${2}

	#
	# Step 7: Sign the image and add public key to U-Boot dtb
	#
	if [ "x${UBOOT_SIGN_ENABLE}" = "x1" ] ; then
		add_key_to_u_boot=""
		if [ -n "${UBOOT_DTB_BINARY}" ]; then
			# The u-boot.dtb is a symlink to UBOOT_DTB_IMAGE, so we need copy
			# both of them, and don't dereference the symlink.
			cp -P ${STAGING_DATADIR}/u-boot*.dtb ${B}
			add_key_to_u_boot="-K ${B}/${UBOOT_DTB_BINARY}"
		fi
		uboot-mkimage \
			${@'-D "${UBOOT_MKIMAGE_DTCOPTS}"' if len('${UBOOT_MKIMAGE_DTCOPTS}') else ''} \
			-F -k "${UBOOT_SIGN_KEYDIR}" \
			$add_key_to_u_boot \
			-r arch/${ARCH}/boot/${2}
	fi
}
