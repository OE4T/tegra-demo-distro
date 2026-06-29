#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraThermalTest(OERuntimeTestCase):
    """thermal zones reporting sane temps; broken BPMP path shows as zeros or empty."""

    MIN_SANE_ZONES = 4

    def test_zones_report_sane_temp(self):
        status, listing = self.target.run(
            "ls /sys/class/thermal/thermal_zone*/temp 2>/dev/null")
        self.assertTrue(status == 0 and listing.strip(),
                        msg="no thermal zones under /sys/class/thermal/ (BPMP driver failure)")
        sane, zero_stuck, readings = [], [], []
        for path in listing.split():
            _, val = self.target.run("cat %s 2>/dev/null" % path)
            val = val.strip()
            readings.append("%s=%s" % (path, val))
            try:
                milli = int(val)
            except ValueError:
                # a disabled zone (tj-thermal on p3767/p3768) reads empty; skip it
                continue
            if milli == 0:
                zero_stuck.append(path)
                continue
            if -20000 <= milli <= 150000:
                sane.append(path)
        self.assertEqual(zero_stuck, [],
                         msg="thermal zones stuck at 0 (BPMP IPC error): %s" % zero_stuck)
        # several zones reading sane temps proves the BPMP thermal path is healthy
        self.assertGreaterEqual(len(sane), self.MIN_SANE_ZONES,
                                msg="fewer than %d sane thermal zones (BPMP thermal path suspect): %s"
                                    % (self.MIN_SANE_ZONES, readings))
