#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import re

from oeqa.runtime.case import OERuntimeTestCase

class TegraNvbootctrlTest(OERuntimeTestCase):
    """nvbootctrl reports a valid A/B bootloader slot layout."""

    def test_dump_slots(self):
        status, output = self.target.run("nvbootctrl dump-slots-info")
        self.assertEqual(status, 0, msg=output)
        self.assertRegex(output, r"(?mi)^\s*Active bootloader slot:\s*[AB]\b",
                         msg="no active A/B slot reported:\n%s" % output)
        self.assertRegex(output, r"(?mi)^\s*Capsule update status:\s*\d+",
                         msg="no capsule update status reported:\n%s" % output)
        slots = re.search(r"(?mi)^\s*num_slots:\s*(\d+)", output)
        self.assertTrue(slots and int(slots.group(1)) >= 2,
                        msg="fewer than two bootloader slots (no A/B redundancy):\n%s" % output)
