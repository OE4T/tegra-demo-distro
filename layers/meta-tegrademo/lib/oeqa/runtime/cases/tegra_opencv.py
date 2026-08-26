#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.runtime.decorator.package import OEHasPackage

class TegraOpencvTest(OERuntimeTestCase):
    """OpenCV is installed with its CUDA modules."""

    @OEHasPackage(["libopencv-cudaarithm"])
    def test_opencv_cuda(self):
        # the cuda* modules exist only when opencv is built WITH CUDA, so their presence is the check
        status, so_path = self.target.run("ls /usr/lib*/libopencv_cudaarithm.so* 2>/dev/null")
        self.assertTrue(status == 0 and so_path.strip(),
                        msg="opencv CUDA modules not installed (no libopencv_cudaarithm.so*)")
