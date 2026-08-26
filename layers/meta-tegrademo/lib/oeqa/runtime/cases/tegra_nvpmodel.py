#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import re

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.runtime.decorator.package import OERequirePackage
from oeqa.core.decorator.depends import OETestDepends

class TegraNvpmodelTest(OERuntimeTestCase):
    """query the active nvpmodel mode and verify super-mode support."""

    @OERequirePackage(["tegra-nvpmodel"])
    def test_nvpmodel_query(self):
        status, output = self.target.run("nvpmodel -q")
        self.assertEqual(status, 0, msg=output)
        self.assertRegex(output, r"NV Power Mode:\s+\w[\w -]*",
                         msg="no active power mode name: %s" % output)
        m = re.search(r"(?m)^\s*(\d+)\s*$", output)
        self.assertIsNotNone(m, msg="no numeric mode id: %s" % output)

    @OERequirePackage(["tegra-nvpmodel"])
    @OETestDepends(['tegra_versions.TegraVersionsTest.test_l4t_release'])
    def test_nvpmodel_super_mode(self):
        # MAXN_SUPER: absent on Thor; p3767 since R36.4.3; p3701-0000 since R39.2
        _, compat = self.target.run(
            "cat /sys/firmware/devicetree/base/compatible 2>/dev/null | tr '\\000' '\\n'")
        if "tegra264" in compat:
            self.skipTest("Thor (tegra264) has no MAXN_SUPER mode")
        if "p3767-" not in compat and "p3701-0000" not in compat:
            self.skipTest("MAXN_SUPER not defined for this module")
        if "p3701-0000" in compat:
            _, rel = self.target.run("cat /etc/nv_tegra_release 2>/dev/null")
            m = re.search(r"\bR(\d+)\b", rel)
            if not m or int(m.group(1)) < 39:
                self.skipTest("AGX Orin 32GB has MAXN_SUPER only from R39 (release: %s)"
                              % (rel.strip()[:30] or "unknown"))

        status, conf = self.target.run("cat /etc/nvpmodel.conf")
        self.assertEqual(status, 0, msg="nvpmodel config /etc/nvpmodel.conf absent")
        self.assertRegex(conf, r"(?m)^<\s*POWER_MODEL\s+ID=\d+\s+NAME=MAXN_SUPER\s*>",
                         msg="no MAXN_SUPER POWER_MODEL entry in /etc/nvpmodel.conf: %s" % conf[-400:])
        # the super-mode id varies by board (e.g. 2 on p3767-0003, 0 on p3767-0000)
        m = re.search(r"(?m)^<\s*POWER_MODEL\s+ID=(\d+)\s+NAME=MAXN_SUPER\s*>", conf)
        super_id = int(m.group(1))
        status, output = self.target.run("nvpmodel -m %d" % super_id)
        self.assertEqual(status, 0,
                         msg="nvpmodel -m %d (MAXN_SUPER) failed: %s" % (super_id, output))
        try:
            status, output = self.target.run("nvpmodel -q")
            self.assertEqual(status, 0, msg="nvpmodel -q after super switch failed: %s" % output)
            self.assertIn("MAXN_SUPER", output,
                          msg="active mode after -m %d is not MAXN_SUPER: %s" % (super_id, output))
        finally:
            self.target.run("nvpmodel -m 0")  # restore default mode for later tests
