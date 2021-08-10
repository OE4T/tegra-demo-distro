# Overrides for the standard read-only-rootfs ROOTFS_POSTCOMMAND hook.
#
# For our Mender-based builds, we
#  (a) know that we're using systemd, so no need to handle inittab/sysvinit
#  (b) use openssh for sshd, so no need to handle dropbear
#  (c) want to keep the SSH host keys between boots, so we put them on
#      the persistent /var/lib overlay mount, rather than in /var/run.
replacement_read_only_rootfs_hook() {
	# Tweak the mount option and fs_passno for rootfs in fstab
	if [ -f ${IMAGE_ROOTFS}/etc/fstab ]; then
		sed -i -e '/^[#[:space:]]*\/dev\/root/{s/defaults/ro/;s/\([[:space:]]*[[:digit:]]\)\([[:space:]]*\)[[:digit:]]$/\1\20/}' ${IMAGE_ROOTFS}/etc/fstab
	fi

    if [ -d ${IMAGE_ROOTFS}${sysconfdir}/ssh ]; then
        if [ -e ${IMAGE_ROOTFS}${sysconfdir}/ssh/ssh_host_rsa_key ]; then
            echo "SYSCONFDIR=${sysconfdir}/ssh" >> ${IMAGE_ROOTFS}${sysconfdir}/default/ssh
	else
	    echo "SYSCONFDIR=${localstatedir}/lib/ssh" >> ${IMAGE_ROOTFS}${sysconfdir}/default/ssh
	    echo "SSHD_OPTS='-f /etc/ssh/sshd_config_readonly'" >> ${IMAGE_ROOTFS}${sysconfdir}/default/ssh
	    sed -i -e's,^HostKey /var/run/ssh,HostKey ${localstatedir}/lib/ssh,' ${IMAGE_ROOTFS}${sysconfdir}/ssh/sshd_config_readonly
	    sed -i -e'/^\[Service/a StateDirectory=ssh\nRuntimeDirectory=sshd' ${IMAGE_ROOTFS}${systemd_system_unitdir}/sshd@.service
	    sed -i -e'/^ExecStartPre=/d' ${IMAGE_ROOTFS}${systemd_system_unitdir}/sshd.socket
	    sed -i -e's,^RequiresMountsFor=.*,RequiresMountsFor=${localstatedir}/lib /run,' ${IMAGE_ROOTFS}${systemd_system_unitdir}/sshdgenkeys.service
	fi
    fi

    if ${@bb.utils.contains("DISTRO_FEATURES", "systemd", "true", "false", d)}; then
    # Create machine-id
    # 20:12 < mezcalero> koen: you have three options: a) run systemd-machine-id-setup at install time, b) have / read-only and an empty file there (for stateless) and c) boot with / writable
        touch ${IMAGE_ROOTFS}${sysconfdir}/machine-id
    fi
}

ROOTFS_POSTPROCESS_COMMAND:remove:tegrademo-mender = "read_only_rootfs_hook;"
ROOTFS_POSTPROCESS_COMMAND:append:tegrademo-mender = "${@bb.utils.contains('IMAGE_FEATURES', 'read-only-rootfs', ' replacement_read_only_rootfs_hook;', '', d)}"
