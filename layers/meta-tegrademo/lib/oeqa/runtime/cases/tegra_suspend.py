#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import time

from oeqa.runtime.case import OERuntimeTestCase
from tegra_reconnect import TegraReconnect
from oeqa.core.target.ssh import OESSHTarget
from oeqa.core.decorator.data import skipIfQemu
from oeqa.core.decorator.depends import OETestDepends

class TegraSc7AdvertisedTest(OERuntimeTestCase):
    """SC7 (deep sleep) is advertised by the kernel; read-only, so it runs on any target."""

    @skipIfQemu()
    def test_sc7_state_advertised(self):
        # mem = suspend-to-RAM (SC7) on Tegra
        status, output = self.target.run("cat /sys/power/state")
        self.assertEqual(status, 0,
                         msg="/sys/power/state missing (kernel PM not built in?): %s" % output)
        self.assertIn("mem", output.split(),
                      msg="suspend-to-RAM (mem) not advertised in /sys/power/state "
                          "(SC7 gap): %s" % output.strip())

        # deep = SC7 mapping in mem_sleep
        status, output = self.target.run("cat /sys/power/mem_sleep")
        self.assertEqual(status, 0,
                         msg="/sys/power/mem_sleep missing (SC7 not compiled in?): %s" % output)
        self.assertRegex(output, r"\bdeep\b",
                         msg="deep sleep (SC7) not offered by mem_sleep: %s" % output.strip())

class TegraDeepSleepTest(TegraReconnect, OERuntimeTestCase):
    """SC7 deep sleep RTC-wake cycle; needs an SSH target to reconnect."""

    WAKE_AFTER = 30
    RESUME_TIMEOUT = 120

    def _wait_for_resume(self, success_before, started):
        # the board is dark until the RTC fires, so a counter increment seen only
        # after WAKE_AFTER elapsed proves this cycle, not a stray earlier suspend
        deadline = started + self.WAKE_AFTER + self.RESUME_TIMEOUT
        while time.monotonic() < deadline:
            time.sleep(5)
            status, out = self.target.run("cat /sys/power/suspend_stats/success",
                                          timeout=15, ignore_ssh_fails=True)
            if (status == 0 and out.strip().isdigit()
                    and int(out.strip()) > success_before
                    and time.monotonic() - started >= self.WAKE_AFTER):
                return True
        return False

    @skipIfQemu()
    @OETestDepends(['tegra_boottime.TegraBootTest.test_system_running'])
    def test_sc7_rtcwake_cycle(self):
        # the board wakes itself via the on-module RTC alarm (no external source);
        # SSH only, since serial cannot reconnect after the board goes dark
        if not isinstance(self.target, OESSHTarget):
            self.skipTest("SC7 wake cycle needs an SSH target; serial cannot reconnect")
        rtc = self.target.run(
            "for r in /sys/class/rtc/*/wakealarm; do "
            "[ -w \"$r\" ] && echo \"$r\" && break; done")[1].strip()
        self.assertTrue(rtc,
                        msg="no writable RTC wakealarm under /sys/class/rtc/*/wakealarm; "
                            "tegra-rtc node absent or read-only (BSP regression)")
        boot_before = self._boot_id()
        self.assertTrue(boot_before, msg="could not read boot_id before suspend")

        self.target.run("echo 0 > %s" % rtc)
        self.assertEqual(self.target.run("echo +%d > %s" % (self.WAKE_AFTER, rtc))[0], 0,
                         msg="could not arm RTC wakealarm at %s; PMC wakeup IRQ path broken" % rtc)
        status, succ = self.target.run("cat /sys/power/suspend_stats/success")
        self.assertEqual(status, 0,
                         msg="/sys/power/suspend_stats/success missing "
                             "(CONFIG_PM_SLEEP_STATS not enabled?): %s" % succ)
        self.assertTrue(succ.strip().isdigit(),
                        msg="suspend_stats/success not a digit: %r" % succ)
        success_before = int(succ.strip())
        # force SC7 (deep), not s2idle, so the cycle exercises real deep sleep
        self.target.run("echo deep > /sys/power/mem_sleep")
        _, ms = self.target.run("cat /sys/power/mem_sleep")
        self.assertRegex(ms, r"\[deep\]",
                         msg="mem_sleep did not select SC7 (deep); an s2idle cycle would "
                             "false-pass this test: %s" % ms.strip())
        started = time.monotonic()
        self.target.run("(systemctl suspend || echo mem > /sys/power/state) &",
                        timeout=5, ignore_ssh_fails=True)

        self.assertTrue(self._wait_for_resume(success_before, started),
                        msg="suspend counter did not advance after a full SC7 dwell; "
                            "SC7 did not complete (check for a re-suspend loop or an "
                            "enable_irq_wake failure)")
        # an unchanged boot_id proves this was a suspend, not a reboot
        self.assertEqual(self._boot_id(), boot_before,
                         msg="boot_id changed across the cycle; board rebooted, not SC7")

        # resume must leave the rootfs usable: a storage controller that does not
        # come back returns EIO on every later read, which the boot_id check misses
        self.target.run("sync; echo 3 > /proc/sys/vm/drop_caches", ignore_ssh_fails=True)
        status, out = self.target.run("cat /bin/sh > /dev/null && echo ok")
        self.assertEqual(status, 0,
                         msg="rootfs read failed after SC7 resume; storage did not "
                             "resume cleanly (e.g. NVMe EIO): %s" % out)
