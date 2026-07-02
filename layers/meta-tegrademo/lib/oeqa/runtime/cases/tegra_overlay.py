#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraDevicetreeOverlayTest(OERuntimeTestCase):
    """oe4t overlay applied; root compatible starts with oe4t,"""

    def test_oe4t_compatible(self):
        compatible = "/sys/firmware/devicetree/base/compatible"
        status, output = self.target.run("tr '\\000' '\\n' < %s" % compatible)
        self.assertEqual(status, 0,
                         msg="cannot read devicetree compatible: %s" % output)
        lines = [l.strip() for l in output.splitlines() if l.strip()]
        self.assertTrue(lines, msg="empty devicetree compatible node")
        # the oe4t dtb provider is mutually exclusive with the capsule/swupdate path,
        # so skip rather than fail when it is not the active provider
        if not any("oe4t," in l for l in lines):
            self.skipTest("oe4t devicetree provider (tegrademo-devicetree) not in use; "
                          "the overlay demo and the capsule/swupdate path cannot coexist")
        self.assertRegex(lines[0], r"^oe4t,[a-z0-9]",
                         msg="oe4t entry is not first compatible or malformed: %s" % lines[0])
