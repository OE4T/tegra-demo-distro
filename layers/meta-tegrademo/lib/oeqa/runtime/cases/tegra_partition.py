#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraPartitionTest(OERuntimeTestCase):
    """by-partlabel entries present, confirming flash wrote the expected GPT."""

    def test_partlabels(self):
        status, output = self.target.run("ls /dev/disk/by-partlabel/")
        self.assertEqual(status, 0,
                         msg="ls /dev/disk/by-partlabel/ failed (rc=%d): %s" % (status, output))
        self.assertTrue(output.strip(),
                        msg="by-partlabel is empty; GPT was not laid down or udev did not enumerate it")
        labels = output.split()
        # APP is present in every L4T layout (AB and non-AB)
        self.assertIn("APP", labels,
                      msg="APP partlabel missing; named partitions: %s" % output)
