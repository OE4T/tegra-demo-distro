#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraCameraTest(OERuntimeTestCase):
    """Argus CSI capture (e.g. IMX219) with a camera attached; headless."""

    NUM_BUFFERS = 10

    def _require_argus(self):
        # match the plugin listing; a bare gst-inspect of a missing element exits 255 and
        # reads as a dropped connection on the remote target
        status, _ = self.target.run("gst-inspect-1.0 2>/dev/null | grep -qw nvarguscamerasrc")
        self.assertEqual(status, 0, msg="nvarguscamerasrc element not registered; plugin packaging gap")
        if self.target.run("test -S /tmp/argus_socket")[0] != 0:
            self.skipTest("no nvargus-daemon socket; no CSI camera on this board")

    def _capture(self, sensor_id):
        self._require_argus()
        # nvarguscamerasrc exits non-zero on a benign teardown error; judge by the Argus log markers
        _, output = self.target.run(
            "gst-launch-1.0 nvarguscamerasrc sensor-id=%d num-buffers=%d "
            "! 'video/x-raw(memory:NVMM)' ! fakesink" % (sensor_id, self.NUM_BUFFERS))
        if "no cameras available" in output.lower():
            self.skipTest("no CSI sensor on sensor-id=%d" % sensor_id)
        self.assertIn("Starting repeat capture requests", output,
                      msg="Argus did not start capturing on sensor-id=%d:\n%s"
                          % (sensor_id, output[-2000:]))
        self.assertIn("Got EOS", output,
                      msg="capture did not reach EOS (no frames flowed) on sensor-id=%d:\n%s"
                          % (sensor_id, output[-2000:]))

    def test_argus_capture_sensor0(self):
        self._capture(0)

    def test_argus_capture_sensor1(self):
        self._capture(1)

    def test_argus_jpeg(self):
        self._require_argus()
        jpg = "/tmp/tegra-argus.jpg"
        self.target.run("rm -f %s" % jpg)
        _, output = self.target.run(
            "gst-launch-1.0 nvarguscamerasrc sensor-id=0 num-buffers=1 ! "
            "nvvidconv ! nvjpegenc ! filesink location=%s" % jpg)
        if "no cameras available" in output.lower():
            self.skipTest("no CSI sensor on sensor-id=0")
        status, _ = self.target.run("test -s %s" % jpg)
        self.target.run("rm -f %s" % jpg)
        self.assertEqual(status, 0,
                         msg="argus capture produced no JPEG artifact (no real image saved)")
