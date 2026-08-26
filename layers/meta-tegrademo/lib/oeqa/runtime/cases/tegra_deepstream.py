#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.runtime.decorator.package import OEHasPackage

class TegraDeepstreamTest(OERuntimeTestCase):
    """DeepStream sample apps via run-deepstream-tests."""

    @OEHasPackage(["deepstream-tests"])
    def test_deepstream(self):
        status, output = self.target.run("run-deepstream-tests", timeout=1800)
        self.assertEqual(status, 0,
                         msg="run-deepstream-tests reported failures:\n%s" % output[-2000:])
        self.assertRegex(output, r"Tests failed:\s+0",
                         msg="run-deepstream-tests summary not clean:\n%s" % output[-2000:])
        # reject the all-skip false-pass (a stale DEEPSTREAM_PATH skips every sub-test yet exits 0)
        self.assertRegex(output, r"Tests passed:\s+[1-9]",
                         msg="run-deepstream-tests: no sub-tests passed (all skipped or none ran):\n%s" % output[-2000:])
