#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import time

class TegraReconnect:
    """boot_id helpers for cases that reboot or suspend the board. boot_id changes
    on every boot, so it tells a real reboot from a slow link. SSH-only."""

    BOOT_TIMEOUT = 300

    def _boot_id(self):
        for _ in range(6):
            status, out = self.target.run("cat /proc/sys/kernel/random/boot_id",
                                          timeout=30, ignore_ssh_fails=True)
            if status == 0 and out.strip():
                return out.strip()
            time.sleep(5)
        return ""

    def _wait_for_new_boot(self, previous):
        deadline = time.monotonic() + self.BOOT_TIMEOUT
        while time.monotonic() < deadline:
            time.sleep(5)
            status, out = self.target.run("cat /proc/sys/kernel/random/boot_id",
                                          timeout=15, ignore_ssh_fails=True)
            if status == 0 and out.strip() and out.strip() != previous:
                return out.strip()
        return ""
