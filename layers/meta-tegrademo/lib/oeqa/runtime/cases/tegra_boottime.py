#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import time

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends

class TegraBootTest(OERuntimeTestCase):
    """System reached a healthy state after boot."""

    SYSTEMCTL = "SYSTEMD_BUS_TIMEOUT=300s systemctl"

    def _failed_units(self):
        _, failed = self.target.run(
            "COLUMNS=400 SYSTEMD_COLORS=0 %s list-units --state=failed "
            "--no-legend --plain --no-pager | awk '{print $1}'" % self.SYSTEMCTL)
        return failed

    # no dependency: the state-changing cases depend on boottime, not the reverse
    def test_system_running(self):
        status, output = self.target.run("command -v systemctl")
        self.assertEqual(status, 0,
                         msg="systemctl not found on demo-image-full: %s" % output)
        # poll up to 3 min; a fresh-flash first boot settles slower (first-boot
        # services and the OTA bootloader-update verifier) than a warm reboot
        state = ""
        endtime = time.time() + 180
        while True:
            _, state = self.target.run("%s is-system-running" % self.SYSTEMCTL)
            state = state.strip()
            if state.startswith(("running", "degraded")):
                break
            if time.time() >= endtime:
                break
            time.sleep(5)
        failed = self._failed_units() if state == "degraded" else ""
        self.assertRegex(state, r"^(running|degraded)",
                         msg="system not running/degraded after wait: %s\nfailed units:\n%s"
                             % (state, failed))

    @OETestDepends(['tegra_boottime.TegraBootTest.test_system_running'])
    def test_no_failed_units(self):
        # networkd-wait-online is benign when the bench has no DHCP for this NIC
        benign = {"systemd-networkd-wait-online.service"}
        real = [u for u in self._failed_units().split() if u and u not in benign]
        if real:
            _, detail = self.target.run(
                "%s status --full --failed --no-pager" % self.SYSTEMCTL)
            self.fail("failed systemd units after boot: %s\n%s" % (" ".join(real), detail))
