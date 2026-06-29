#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.runtime.decorator.package import OEHasPackage

class TegraTensorrtTest(OERuntimeTestCase):
    """TensorRT sample engines via run-tensorrt-tests."""

    @OEHasPackage(["tensorrt-tests"])
    def test_tensorrt(self):
        status, output = self.target.run("run-tensorrt-tests", timeout=900)
        self.assertEqual(status, 0,
                         msg="run-tensorrt-tests reported failures:\n%s" % output)
        self.assertRegex(output, r"Tests passed:\s+[1-9]",
                         msg="no tensorrt sample passed (all skipped?):\n%s" % output[-2000:])
