#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from tegra_reconnect import TegraReconnect
from oeqa.runtime.decorator.package import OEHasPackage
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.target.ssh import OESSHTarget

class TegraCapsuleTest(TegraReconnect, OERuntimeTestCase):
    """UEFI capsule update of the non-current bootloader slot."""

    BOOT_TIMEOUT = 600
    ESP = "/boot/efi"
    CAPSULE = "/opt/nvidia/UpdateCapsule/tegra-bl.cap"

    def _dump_slots_info(self):
        status, info = self.target.run("nvbootctrl dump-slots-info")
        self.assertEqual(status, 0, msg="nvbootctrl dump-slots-info failed: %s" % info)
        return info

    @OEHasPackage(["tegra-uefi-capsules"])
    @OETestDepends(['tegra_esrt.TegraEsrtTest.test_esrt_present',
                    'tegra_boottime.TegraBootTest.test_system_running'])
    def test_capsule_update_cycle(self):
        if not isinstance(self.target, OESSHTarget):
            self.skipTest("capsule update needs an SSH target; serial cannot reconnect")

        status, _ = self.target.run("test -f %s" % self.CAPSULE)
        self.assertEqual(status, 0,
                         msg="capsule payload %s missing despite tegra-uefi-capsules" % self.CAPSULE)

        before = self._dump_slots_info()
        self.assertRegex(before, r"(?mi)^\s*Capsule update status:\s*0\b",
                         msg="capsule status not 0 before update:\n%s" % before)

        status, out = self.target.run(
            "mkdir -p %s/EFI/UpdateCapsule && cp %s %s/EFI/UpdateCapsule/ && sync"
            % (self.ESP, self.CAPSULE, self.ESP))
        self.assertEqual(status, 0, msg="cannot stage the capsule on the ESP: %s" % out)

        # request capsule-on-disk processing on the next boot
        status, out = self.target.run("oe4t-set-uefi-OSIndications")
        self.assertEqual(status, 0, msg="cannot set the OsIndications capsule bit: %s" % out)

        boot_before = self._boot_id()
        self.assertTrue(boot_before, msg="could not read boot_id before the capsule reboot")
        self.target.run("reboot", timeout=10, ignore_ssh_fails=True)
        self.assertTrue(self._wait_for_new_boot(boot_before),
                        msg="board did not reboot and return within %ds after the capsule" % self.BOOT_TIMEOUT)

        after = self._dump_slots_info()
        self.assertRegex(after, r"(?mi)^\s*Capsule update status:\s*1\b",
                         msg="capsule update status not 1 after reboot (apply failed):\n%s" % after)

        # every FMP entry must report success; a failed capsule leaves its entry non-zero,
        # so checking that no entry failed catches it without parsing the capsule's GUID
        status, st = self.target.run(
            "cat /sys/firmware/efi/esrt/entries/entry*/last_attempt_status")
        self.assertEqual(status, 0, msg="no ESRT entries; capsule path not firmware-backed")
        failed = [v for v in st.split() if v.strip() != "0"]
        self.assertEqual(failed, [],
                         msg="an ESRT entry reports a failed capsule update "
                             "(last_attempt_status != 0):\n%s" % st)
