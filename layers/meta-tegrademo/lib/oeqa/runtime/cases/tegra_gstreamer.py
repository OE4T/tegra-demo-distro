#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.runtime.decorator.package import OERequirePackage

class TegraGstreamerTest(OERuntimeTestCase):
    """NVJPEG and NVDEC/NVENC pipelines; codecs to fakesink, canned scripts to nv3dsink."""

    X = "DISPLAY=:0 XAUTHORITY=/root/.Xauthority"

    def _element(self, name):
        # gst-inspect <element> exits 255 when the element is missing, which OESSHTarget
        # cannot tell from an ssh failure; assert against the plugin listing instead
        status, _ = self.target.run("gst-inspect-1.0 2>/dev/null | grep -qw %s" % name)
        self.assertEqual(status, 0, msg="gstreamer element %s not registered; plugin packaging gap" % name)

    def _pipeline(self, desc):
        status, output = self.target.run("gst-launch-1.0 " + desc, timeout=120)
        self.assertEqual(status, 0, msg="pipeline failed:\n%s\n%s" % (desc, output[-2000:]))
        self.assertIn("Got EOS", output,
                      msg="pipeline produced no EOS (no frames flowed):\n%s" % output[-2000:])

    def test_nvjpeg(self):
        self._element("nvjpegenc")
        self._element("nvjpegdec")
        self._pipeline("videotestsrc num-buffers=10 ! 'video/x-raw,width=640,height=480,format=I420' "
                       "! nvjpegenc ! nvjpegdec ! fakesink")

    def test_h264_codec(self):
        self._element("nvv4l2decoder")
        if self.target.run("gst-inspect-1.0 nvvideo4linux2 2>/dev/null | grep -q nvv4l2h264enc")[0] != 0:
            self.skipTest("no NVENC encoder on this SKU")
        self._pipeline("videotestsrc num-buffers=30 ! 'video/x-raw,width=640,height=480' "
                       "! nvvidconv ! 'video/x-raw(memory:NVMM)' ! nvv4l2h264enc ! h264parse "
                       "! nvv4l2decoder ! fakesink")

    @OERequirePackage(["gstreamer-tests"])
    def test_display_pipelines(self):
        # sinteltest renders through nv3dsink, nvjpegtest through xvimagesink, both on Xorg :0;
        # the egl/weston images run no X server, so skip there rather than force a missing :0
        if self.target.run("pgrep -x Xorg")[0] != 0:
            self.skipTest("no X server; the nv3dsink display pipelines need Xorg :0")
        for script in ("nvjpegtest", "sinteltest"):
            status, output = self.target.run("%s %s" % (self.X, script), timeout=240)
            self.assertEqual(status, 0, msg="%s failed:\n%s" % (script, output[-2000:]))
            self.assertNotIn("ERROR", output, msg="%s pipeline error:\n%s" % (script, output[-2000:]))
