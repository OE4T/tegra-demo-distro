#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.runtime.decorator.package import OEHasPackage

class TegraDisplayTest(OERuntimeTestCase):
    """DRM is up and a monitor is detected on the display output."""

    def test_drm_device_present(self):
        status, output = self.target.run("ls /sys/class/drm/ 2>/dev/null")
        self.assertTrue(status == 0 and "card" in output,
                        msg="no DRM subsystem (no /sys/class/drm/card*); display driver not loaded")
        self.assertRegex(output, r"card\d+", msg="no DRM device: %s" % output)

    @OEHasPackage(["xrandr"])
    def test_display_connected(self):
        # xrandr-gated, so this runs only on the X11 images (xrandr comes with x11-base),
        # where Xorg is up; a dead Xorg makes xrandr fail and the test fail, as intended
        X = "DISPLAY=:0 XAUTHORITY=/root/.Xauthority"
        status, output = self.target.run("%s xrandr --query" % X)
        self.assertEqual(status, 0, msg="xrandr query failed:\n%s" % output)
        self.assertRegex(output, r"(DP|HDMI)[-0-9]* connected",
                         msg="no DP/HDMI output connected; bench monitor missing or not detected:\n%s" % output)
        _, verbose = self.target.run("%s xrandr --verbose" % X)
        self.assertRegex(verbose, r"EDID:\s*\n\s+00ffffffffffff00",
                         msg="no valid EDID on the connected output:\n%s" % verbose[-1500:])
