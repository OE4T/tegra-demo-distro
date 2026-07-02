#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends

class TegraNetworkTest(OERuntimeTestCase):
    """Physical NIC present with a live carrier."""

    def test_nic_present(self):
        # virtual ifaces (lo, bridges) have no device symlink; judge by output not status
        _, output = self.target.run(
            "for n in /sys/class/net/*; do [ -e \"$n/device\" ] && basename \"$n\"; done")
        self.assertTrue(output.strip(),
                        msg="no physical network interface bound (NIC driver not loaded)")

    @OETestDepends(['tegra_network.TegraNetworkTest.test_nic_present'])
    def test_carrier(self):
        # read carrier only for physical ifaces; lo and bridges/veth always report 1
        _, out = self.target.run(
            "for n in /sys/class/net/*; do [ -e \"$n/device\" ] && cat \"$n/carrier\" 2>/dev/null; done")
        self.assertIn("1", out.split(),
                      msg="no physical NIC reports a live carrier (no cable attached): %s" % out)
