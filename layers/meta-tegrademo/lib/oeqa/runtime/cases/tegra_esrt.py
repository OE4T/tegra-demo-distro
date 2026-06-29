#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraEsrtTest(OERuntimeTestCase):
    """ESRT present and populated; prerequisite gate for capsule/swupdate tests."""

    def test_esrt_present(self):
        # efi=runtime in KERNEL_ARGS means /sys/firmware/efi must exist; edk2-nvidia FMP populates ESRT
        status, _ = self.target.run("test -d /sys/firmware/efi")
        self.assertEqual(status, 0, msg="EFI sysfs absent; system must boot via edk2-nvidia")

        status, _ = self.target.run("test -d /sys/firmware/efi/esrt")
        self.assertEqual(status, 0, msg="ESRT sysfs dir absent; edk2-nvidia FMP should expose it")

        _, entry = self.target.run(
            "ls -d /sys/firmware/efi/esrt/entries/*/ 2>/dev/null | head -n1")
        entry = entry.strip()
        self.assertTrue(entry, msg="ESRT entries/ empty; FMP firmware should populate at least one entry")

        status, fw_class = self.target.run("cat %sfw_class" % entry)
        self.assertEqual(status, 0, msg="ESRT entry has no fw_class: %s" % fw_class)
        self.assertRegex(
            fw_class.strip(),
            r"(?i)^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            msg="ESRT fw_class is not a GUID: %s" % fw_class)

        status, fw_version = self.target.run("cat %sfw_version" % entry)
        self.assertEqual(status, 0, msg="ESRT entry has no fw_version: %s" % fw_version)
        self.assertRegex(fw_version.strip(), r"^\d+$",
                         msg="ESRT fw_version is not a decimal integer: %s" % fw_version)
