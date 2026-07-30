#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraSamplesTest(OERuntimeTestCase):
    """headless CUDA sample binaries from cuda-samples."""

    def _run(self, path, name, expect=None):
        status, _ = self.target.run("test -x %s" % path)
        self.assertEqual(status, 0, msg="%s not installed; cuda-samples packaging gap" % name)
        status, output = self.target.run(path)
        self.assertEqual(status, 0, msg="%s failed:\n%s" % (name, output))
        if expect:
            self.assertRegex(output, expect,
                             msg="%s: success not confirmed:\n%s" % (name, output))

    def test_cuda_devicequery(self):
        self._run("/usr/bin/cuda-samples/deviceQuery", "cuda deviceQuery",
                  expect=r"Result = PASS")

    def test_cuda_unified_memory(self):
        self._run("/usr/bin/cuda-samples/UnifiedMemoryStreams", "cuda UnifiedMemoryStreams",
                  expect=r"All Done!")

    def test_cuda_vectoradd(self):
        self._run("/usr/bin/cuda-samples/vectorAdd", "cuda vectorAdd", expect=r"Test PASSED")
