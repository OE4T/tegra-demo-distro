#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraIdentityTest(OERuntimeTestCase):
    """kernel version and devicetree identity checks."""

    def test_kernel_version(self):
        status, output = self.target.run("uname -r")
        self.assertEqual(status, 0, msg="uname failed: %s" % output)
        self.assertRegex(output.strip(), r"^\d+\.\d+\.\d+",
                         msg="unexpected kernel version: %s" % output)

    def test_devicetree_compatible(self):
        # NUL-separated list; redirect avoids head exit masking a missing node
        status, output = self.target.run(
            "tr '\\000' '\\n' < /sys/firmware/devicetree/base/compatible")
        if status != 0:
            self.skipTest("no devicetree compatible node")
        lines = [l.strip() for l in output.splitlines() if l.strip()]
        if not lines:
            self.skipTest("empty devicetree compatible node")
        compatible = lines[0]
        # nvidia, = stock; oe4t, = demo overlay prefix
        self.assertRegex(compatible, r"^(nvidia|oe4t),[a-z0-9]",
                         msg="unexpected board compatible: %s" % compatible)

    def test_devicetree_model(self):
        status, output = self.target.run(
            "tr -d '\\000' < /sys/firmware/devicetree/base/model")
        if status != 0:
            self.skipTest("no devicetree model node")
        self.assertRegex(output, r"(?i)jetson|orin|tegra|nvidia",
                         msg="unexpected board model: %s" % output)
