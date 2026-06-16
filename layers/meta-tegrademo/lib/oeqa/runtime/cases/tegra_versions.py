#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import os
import re

from oeqa.runtime.case import OERuntimeTestCase

class TegraVersionsTest(OERuntimeTestCase):
    """Floor-check L4T and CUDA versions against env vars."""

    # source conf/jetpack-<release>.env before oe-test so the floors are set

    def test_l4t_release(self):
        status, output = self.target.run("cat /etc/nv_tegra_release 2>/dev/null")
        self.assertTrue(status == 0 and output.strip(),
                        msg="/etc/nv_tegra_release absent (nv-tegra-release not installed)")
        m = re.search(r"R(\d+)\b.*?REVISION:\s*([\d.]+)", output)
        self.assertIsNotNone(m, msg="unparseable L4T release: %s" % output)
        want = os.environ["TEGRA_L4T_MAJOR"]
        self.assertEqual(m.group(1), want,
                         msg="L4T major %s != expected %s" % (m.group(1), want))

    def test_cuda_version(self):
        # meta-tegra ships no bare cuda symlink, so find the versioned toolkit dir
        status, dirs = self.target.run("ls -d /usr/local/cuda-*/ 2>/dev/null")
        if status != 0 or not dirs.strip():
            self.skipTest("CUDA toolkit not installed (no /usr/local/cuda-* dir)")
        nvcc = dirs.split()[0].rstrip("/") + "/bin/nvcc"
        status, output = self.target.run("%s --version" % nvcc)
        self.assertEqual(status, 0, msg="nvcc --version failed: %s" % output)
        m = re.search(r"release\s+(\d+)\.(\d+)", output)
        self.assertIsNotNone(m, msg="unparseable CUDA version: %s" % output[:500])
        floor = os.environ["TEGRA_CUDA_MIN"]
        got = tuple(int(x) for x in m.group(1, 2))
        want = tuple(int(x) for x in floor.split(".")[:2])
        self.assertGreaterEqual(got, want,
                                msg="CUDA %s.%s below floor %s" % (m.group(1), m.group(2), floor))
