#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.runtime.decorator.package import OERequirePackage

class TegraMmapiTest(OERuntimeTestCase):
    """MMAPI codec, JPEG, and convert samples via run-mmapi-tests."""

    SAMPLES = ("video_decode video_dec_cuda jpeg_decode jpeg_encode video_convert "
               "decode_sample transform_sample")
    SAMPLES_ENCODE = "video_encode video_cuda_enc encode_sample"

    def _run(self, samples):
        status, output = self.target.run(
            "DISPLAY=:0 XAUTHORITY=/root/.Xauthority run-mmapi-tests %s" % samples,
            timeout=900)
        self.assertEqual(status, 0, msg="mmapi samples failed:\n%s" % output[-3000:])
        self.assertRegex(output, r"Tests passed:\s+[1-9]",
                         msg="no mmapi sample passed:\n%s" % output[-3000:])

    @OERequirePackage(["tegra-mmapi-tests"])
    def test_mmapi_samples(self):
        self._run(self.SAMPLES)

    @OERequirePackage(["tegra-mmapi-tests"])
    def test_mmapi_encode(self):
        # gate on the encoder device node, the same check run-mmapi-tests uses for its encode
        # subtests; the gst element can register without the node and would false-fail the run
        if self.target.run("test -c /dev/v4l2-nvenc")[0] != 0:
            self.skipTest("no NVENC encoder on this SKU")
        self._run(self.SAMPLES_ENCODE)
