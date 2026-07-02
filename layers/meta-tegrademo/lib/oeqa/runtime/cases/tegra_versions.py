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

    # source conf/jetpack-<release>.env before oe-test so the TEGRA_* floors are set;
    # an unset floor is a misconfigured harness and must fail, not silently pass

    def _nv_tegra_release(self):
        # absence is a packaging gap, not a skip
        status, output = self.target.run("cat /etc/nv_tegra_release 2>/dev/null")
        self.assertTrue(status == 0 and output.strip(),
                        msg="/etc/nv_tegra_release absent (nv-tegra-release not installed)")
        return output

    def test_l4t_release(self):
        output = self._nv_tegra_release()
        m = re.search(r"R(\d+)\b.*?REVISION:\s*([\d.]+)", output)
        self.assertIsNotNone(m, msg="unparseable L4T release: %s" % output)
        want = (os.environ.get("TEGRA_L4T_MAJOR") or "").strip()
        self.assertTrue(want, msg="TEGRA_L4T_MAJOR not set")
        self.assertEqual(m.group(1), want,
                         msg="L4T major %s != expected %s" % (m.group(1), want))

    def test_l4t_revision(self):
        output = self._nv_tegra_release()
        m = re.search(r"REVISION:\s*([\d.]+)", output)
        self.assertIsNotNone(m, msg="REVISION field absent in nv_tegra_release: %s" % output)
        want = (os.environ.get("TEGRA_L4T_MINOR") or "").strip()
        self.assertTrue(want, msg="TEGRA_L4T_MINOR not set")
        self.assertEqual(m.group(1), want,
                         msg="L4T revision %s != expected %s" % (m.group(1), want))

    def test_cuda_version(self):
        # no nvcc in the runtime image; read the version from the install dir
        status, dirs = self.target.run("ls -d /usr/local/cuda-*/ 2>/dev/null")
        self.assertTrue(status == 0 and dirs.strip(),
                        msg="CUDA not installed: no /usr/local/cuda-* dir found "
                            "(cuda-libraries packaging gap)")
        # pick the highest cuda-X.Y dir here rather than relying on target sort/tail
        vers = re.findall(r"/cuda-(\d+)\.(\d+)", dirs)
        self.assertTrue(vers, msg="unparseable CUDA install dir: %s" % dirs)
        got = max((int(a), int(b)) for a, b in vers)
        floor = (os.environ.get("TEGRA_CUDA_MIN") or "").strip()
        self.assertTrue(floor, msg="TEGRA_CUDA_MIN not set")
        want = tuple(int(x) for x in floor.split(".")[:2])
        self.assertGreaterEqual(got, want,
                                msg="CUDA %d.%d below floor %s" % (got[0], got[1], floor))
