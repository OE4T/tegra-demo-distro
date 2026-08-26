#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraWatchdogTest(OERuntimeTestCase):
    """watchdog device registered; presence only, not triggered."""

    def test_watchdog_present(self):
        # tegra-wdt is mandatory; absence is a fault
        status, _ = self.target.run("test -c /dev/watchdog || test -c /dev/watchdog0")
        self.assertEqual(status, 0, msg="no /dev/watchdog device node")
        status, output = self.target.run("ls /sys/class/watchdog/ 2>/dev/null")
        self.assertEqual(status, 0, msg="no /sys/class/watchdog/ directory (output: %r)" % output)
        self.assertRegex(output, r"watchdog\d+", msg="no registered watchdog in sysfs: %s" % output)
