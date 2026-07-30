#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import os
import re

from oeqa.runtime.case import OERuntimeTestCase

class TegraIdentityTest(OERuntimeTestCase):
    """kernel version and devicetree identity checks."""

    def test_kernel_version(self):
        status, output = self.target.run("uname -r")
        self.assertEqual(status, 0, msg="uname failed: %s" % output)
        ver = output.strip()
        # require a suffix (e.g. -l4t-r36.5.0-1021.21 or -yocto-standard);
        # a bare x.y.z string means the kernel was not built by this BSP
        self.assertRegex(ver, r"^\d+\.\d+\.\d+.+",
                         msg="unexpected kernel version format: %s" % ver)
        self.assertIn("TEGRA_KERNEL_MIN", os.environ,
                      msg="TEGRA_KERNEL_MIN not set: misconfigured harness (source jetpack-*.env)")
        floor = os.environ["TEGRA_KERNEL_MIN"].strip()
        m = re.match(r"(\d+)\.(\d+)", ver)
        self.assertIsNotNone(m, msg="unparseable kernel version: %s" % ver)
        got = (int(m.group(1)), int(m.group(2)))
        want = tuple(int(x) for x in floor.split(".")[:2])
        self.assertGreaterEqual(got, want,
                                msg="kernel %s below floor %s" % (ver, floor))

    def test_devicetree_compatible(self):
        # the node is always present on a booted Tegra, so a read failure is a
        # transport error, not a reason to skip
        status, output = self.target.run(
            "tr '\\000' '\\n' < /sys/firmware/devicetree/base/compatible")
        self.assertEqual(status, 0, msg="cannot read devicetree compatible: %s" % output)
        lines = [l.strip() for l in output.splitlines() if l.strip()]
        self.assertTrue(lines, msg="empty devicetree compatible node")
        self.assertRegex(lines[0], r"^(nvidia|oe4t),[a-z0-9]",
                         msg="unexpected board compatible: %s" % lines[0])

    def test_devicetree_model(self):
        status, output = self.target.run(
            "tr -d '\\000' < /sys/firmware/devicetree/base/model")
        self.assertEqual(status, 0, msg="cannot read devicetree model: %s" % output)
        self.assertIn("NVIDIA Jetson", output,
                      msg="unexpected board model: %s" % output)
