#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraVpiTest(OERuntimeTestCase):
    """VPI sample suite across the backends the SKU provides."""

    def test_vpi_samples(self):
        # the harness ships as run-vpi-tests plus a release-versioned symlink (run-vpi4-tests on
        # R39); glob for it and skip cleanly rather than gate on a versioned package
        _, harness = self.target.run("ls /usr/bin/run-vpi*-tests 2>/dev/null | head -n 1")
        harness = harness.strip()
        if not harness:
            self.skipTest("no run-vpi*-tests harness installed (vpi-tests package absent)")
        status, output = self.target.run(harness, timeout=1800)
        self.assertEqual(status, 0, msg="%s reported failures:\n%s" % (harness, output[-2000:]))
        self.assertRegex(output, r"Tests passed:\s+[1-9]",
                         msg="no VPI sample passed:\n%s" % output[-2000:])
