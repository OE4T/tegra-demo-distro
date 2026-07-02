#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.runtime.decorator.package import OERequirePackage

class TegraVulkanTest(OERuntimeTestCase):
    """vulkaninfo enumerates the Tegra GPU through the NVIDIA proprietary driver (headless)."""

    @OERequirePackage(["vulkan-tools"])
    @OERequirePackage(["tegra-libraries-vulkan"])
    def test_vulkaninfo(self):
        status, output = self.target.run("vulkaninfo")
        self.assertEqual(status, 0, msg="vulkaninfo failed to run:\n%s" % output[-2000:])
        # require the NVIDIA proprietary driver, not the gfxstream/virtio fallback ICDs
        self.assertIn("DRIVER_ID_NVIDIA_PROPRIETARY", output,
                      msg="Vulkan did not load the NVIDIA driver (software/virtio fallback):\n%s"
                          % output[-2000:])
        self.assertRegex(output, r"deviceType\s*=\s*PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU",
                         msg="Vulkan device is not the integrated Tegra GPU:\n%s" % output[-2000:])
