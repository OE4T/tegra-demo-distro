#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.core.target.ssh import OESSHTarget
from oeqa.runtime.case import OERuntimeTestCase

class TegraOpteeTest(OERuntimeTestCase):
    """OP-TEE device node present and xtest regression passes."""

    def test_tee_device(self):
        status, _ = self.target.run("test -c /dev/tee0 || test -c /dev/teepriv0")
        self.assertEqual(status, 0,
                         msg="no OP-TEE device node (/dev/tee0, /dev/teepriv0); TEE driver not loaded")

    def test_xtest_regression(self):
        # xtest floods the secure-world UART, desyncing a serial console; run over SSH
        if not isinstance(self.target, OESSHTarget):
            self.skipTest("xtest regression needs an SSH target; serial cannot reconnect")
        self.assertEqual(self.target.run("command -v xtest")[0], 0,
                         msg="xtest (optee-test) not installed; packaging gap")
        self.assertEqual(self.target.run("pidof tee-supplicant")[0], 0,
                         msg="tee-supplicant not running; OP-TEE stack is broken")
        # xtest exit code is the pass/fail signal; redirect its console flood to a file
        status, _ = self.target.run("xtest 1001 >/tmp/xtest.1001.log 2>&1")
        _, output = self.target.run("tail -c 2000 /tmp/xtest.1001.log")
        self.assertEqual(status, 0, msg="xtest 1001 failed:\n%s" % output)
