#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import os

from oeqa.runtime.case import OERuntimeTestCase
from tegra_reconnect import TegraReconnect
from oeqa.core.target.ssh import OESSHTarget
from oeqa.core.decorator.data import skipIfQemu
from oeqa.core.decorator.depends import OETestDepends

class TegraRollingRebootTest(TegraReconnect, OERuntimeTestCase):
    """reboot survival; the rolling loop needs an SSH target to reconnect."""

    REBOOT_MISSING = "reboot command not found; INIT_MANAGER=systemd must provide it"

    @skipIfQemu()
    def test_reboot_command_present(self):
        status, output = self.target.run("command -v reboot")
        self.assertEqual(status, 0, msg=self.REBOOT_MISSING)
        self.assertTrue(output.strip(),
                        msg="reboot command resolved to empty path: %s" % output)

    @skipIfQemu()
    @OETestDepends(['tegra_boottime.TegraBootTest.test_system_running'])
    def test_rolling_reboot(self):
        # serial cannot log back in once the board goes dark; the SSH target opens
        # a fresh connection per command, so it survives the reboot drop
        if not isinstance(self.target, OESSHTarget):
            self.skipTest("rolling reboot needs an SSH target; serial cannot reconnect")
        status, _ = self.target.run("command -v reboot")
        self.assertEqual(status, 0, msg=self.REBOOT_MISSING)
        # default 3 for routine gating; the CSV matrix run sets TEGRA_REBOOT_CYCLES higher
        cycles = max(1, int(os.environ.get("TEGRA_REBOOT_CYCLES", "3")))

        boot_id = self._boot_id()
        self.assertTrue(boot_id, msg="could not read boot_id before reboot")
        for cycle in range(1, cycles + 1):
            self.target.run("sync; (sleep 1; reboot) >/dev/null 2>&1 &",
                            timeout=10, ignore_ssh_fails=True)
            boot_id = self._wait_for_new_boot(boot_id)
            self.assertTrue(boot_id,
                            msg="cycle %d/%d: no new boot_id within %ds; board did not "
                                "reboot and return" % (cycle, cycles, self.BOOT_TIMEOUT))
