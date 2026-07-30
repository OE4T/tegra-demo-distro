#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT

import os
import subprocess
import time

from oeqa.core.target.ssh import OESSHTarget


class TegraTarget(OESSHTarget):

    def __init__(self, logger, ip, server_ip, powercontrol_cmd=None,
                 powercontrol_extra_args="", **kwargs):
        super(TegraTarget, self).__init__(logger, ip, server_ip, **kwargs)
        self.powercontrol_cmd = powercontrol_cmd
        if powercontrol_cmd and powercontrol_extra_args:
            self.powercontrol_cmd = "%s %s" % (powercontrol_cmd, powercontrol_extra_args)
        self.flashcontrol_cmd = os.environ.get("TEST_FLASHCONTROL_CMD") or None
        self.flash_artifact = os.environ.get("TEST_FLASHCONTROL_ARTIFACT") or None
        self.boot_timeout = int(os.environ.get("TEST_RCM_BOOT_TIMEOUT") or "300")

    def _host_cmd(self, cmd):
        # runs on the host, not the DUT.
        self.logger.info("TegraTarget host: %s" % cmd)
        return subprocess.call(cmd, shell=True)

    def _power(self, action):
        # on/off/cycle appended as final arg (oe-core convention).
        if self.powercontrol_cmd:
            self._host_cmd("%s %s" % (self.powercontrol_cmd, action))

    def _flash(self):
        if not self.flashcontrol_cmd or not self.flash_artifact:
            self.logger.info("TegraTarget: no TEST_FLASHCONTROL_CMD/ARTIFACT in the "
                             "environment; assuming the board is already flashed")
            return
        self.logger.info("TegraTarget: recovering and flashing %s" % self.flash_artifact)
        rc = self._host_cmd("%s %s" % (self.flashcontrol_cmd, self.flash_artifact))
        if rc != 0:
            raise AssertionError("flash command returned %d: %s %s"
                                 % (rc, self.flashcontrol_cmd, self.flash_artifact))

    def _wait_for_ssh(self):
        # initrd-flash plus first boot is slow, so use a generous boot timeout.
        deadline = time.time() + self.boot_timeout
        while time.time() < deadline:
            status, _ = self.run("true", timeout=30, ignore_ssh_fails=True)
            if status == 0:
                return
            time.sleep(5)
        raise AssertionError("DUT %s did not answer over SSH within %ds"
                             % (self.ip, self.boot_timeout))

    def start(self, **kwargs):
        self._flash()
        self._power("on")
        self._wait_for_ssh()

    def stop(self, **kwargs):
        self._power("off")
