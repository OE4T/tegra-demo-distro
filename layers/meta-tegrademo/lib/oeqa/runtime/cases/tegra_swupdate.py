#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import os

from oeqa.runtime.case import OERuntimeTestCase
from tegra_reconnect import TegraReconnect
from oeqa.runtime.decorator.package import OERequirePackage
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.target.ssh import OESSHTarget

class TegraSwupdateTest(TegraReconnect, OERuntimeTestCase):
    """swupdate A/B install and slot flip; needs a redundant-layout image and SSH."""

    # the capsule (bootloader) update can add minutes to the first reboot
    BOOT_TIMEOUT = 600
    SWU_ON_DUT = "/tmp/tegra-swupdate-test.swu"

    def _current_slot(self):
        status, out = self.target.run("nvbootctrl get-current-slot")
        self.assertEqual(status, 0, msg="nvbootctrl get-current-slot failed: %s" % out)
        self.assertRegex(out.strip(), r"^[01]$", msg="unexpected current slot: %s" % out)
        return out.strip()

    def _dump_slots_info(self):
        status, info = self.target.run("nvbootctrl dump-slots-info")
        self.assertEqual(status, 0, msg="nvbootctrl dump-slots-info failed: %s" % info)
        return info

    @OERequirePackage(["swupdate"])
    @OETestDepends(['tegra_esrt.TegraEsrtTest.test_esrt_present',
                    'tegra_boottime.TegraBootTest.test_system_running'])
    def test_ab_swupdate_cycle(self):
        if not isinstance(self.target, OESSHTarget):
            self.skipTest("A/B swupdate needs an SSH target; serial cannot reconnect")

        status, _ = self.target.run("test -b /dev/disk/by-partlabel/APP_b")
        self.assertEqual(status, 0,
                         msg="no APP_b partition; image not built with USE_REDUNDANT_FLASH_LAYOUT")

        # nvbootctrl MUST be present when both swupdate and redundant layout are present
        status, out = self.target.run("command -v nvbootctrl")
        self.assertEqual(status, 0,
                         msg="nvbootctrl missing despite redundant layout; broken package deps: %s" % out)

        swu = os.environ.get("SWUPDATE_SWU_HOST_PATH", "")
        if swu and os.path.isfile(swu):
            self.target.copyTo(swu, self.SWU_ON_DUT)
        # artifact must exist on DUT; missing .swu on the swupdate image is a real failure
        swu_present = self.target.run("test -f %s" % self.SWU_ON_DUT)[0]
        self.assertEqual(swu_present, 0,
                         msg=".swu not on DUT at %s; set SWUPDATE_SWU_HOST_PATH or pre-place it"
                             % self.SWU_ON_DUT)

        info = self._dump_slots_info()
        self.assertRegex(info, r"(?mi)^\s*Capsule update status:\s*0\b",
                         msg="capsule update status not 0 before update:\n%s" % info)

        slot_before = self._current_slot()
        boot_before = self._boot_id()
        status, output = self.target.run("swupdate -i %s" % self.SWU_ON_DUT, timeout=600)
        self.assertEqual(status, 0,
                         msg="swupdate -i failed (%d):\n%s" % (status, output[-2000:]))

        self.target.run("reboot", timeout=10, ignore_ssh_fails=True)
        self.assertTrue(self._wait_for_new_boot(boot_before),
                        msg="board did not reboot and return within %ds after swupdate"
                            % self.BOOT_TIMEOUT)

        info = self._dump_slots_info()
        self.assertRegex(info, r"(?mi)^\s*Capsule update status:\s*1\b",
                         msg="capsule update status not 1 after first reboot:\n%s" % info)

        slot_after = self._current_slot()
        self.assertNotEqual(slot_after, slot_before,
                            msg="slot did not flip (before=%s after=%s)"
                                % (slot_before, slot_after))

        # second reboot confirms the flipped slot is sticky
        boot_after = self._boot_id()
        self.target.run("reboot", timeout=10, ignore_ssh_fails=True)
        self.assertTrue(self._wait_for_new_boot(boot_after),
                        msg="board did not return within %ds on second reboot"
                            % self.BOOT_TIMEOUT)
        slot_final = self._current_slot()
        self.assertEqual(slot_final, slot_after,
                         msg="slot reverted after second reboot (expected %s, got %s)"
                             % (slot_after, slot_final))
