#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraStorageTest(OERuntimeTestCase):
    """rootfs writable and block-backed after flash+boot."""

    def test_rootfs_writable(self):
        status, output = self.target.run("findmnt -no OPTIONS /")
        self.assertEqual(status, 0, msg="reading root mount failed: %s" % output)
        self.assertRegex(output, r"(^|,)rw(,|$)", msg="rootfs not mounted rw: %s" % output)

    def test_rootfs_on_block_device(self):
        # findmnt resolves the real device behind the /dev/root placeholder
        status, source = self.target.run("findmnt -no SOURCE /")
        self.assertEqual(status, 0, msg="reading root source failed: %s" % source)
        source = source.strip()
        if not source.startswith("/dev/"):
            self.fail("rootfs not block-backed after flash: %s" % source)
        self.assertRegex(source, r"^/dev/(mmcblk|nvme|sd)",
                         msg="rootfs not on expected storage: %s" % source)
