#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import re

from oeqa.runtime.case import OERuntimeTestCase

# TCU=Orin, UTC=Thor, AMA=AGX PL011, S=8250; THS is device-node only (not a console)
_CONSOLE_RE = re.compile(r"(?m)^tty(TCU|UTC|S|AMA)\d+\b")
_DEVNODE_RE = re.compile(r"^/dev/tty(TCU|UTC|THS|S|AMA)\d+$")

class TegraSerialConsoleTest(OERuntimeTestCase):
    """kernel serial console is registered on a Tegra UART."""

    def test_serial_console_registered(self):
        status, output = self.target.run("cat /proc/consoles")
        self.assertEqual(status, 0, msg=output)
        self.assertTrue(_CONSOLE_RE.search(output),
                        msg="no Tegra serial console in /proc/consoles: %s" % output)

    def test_serial_device_node(self):
        _, output = self.target.run("ls /dev/tty* 2>/dev/null")
        nodes = [l for l in output.split() if _DEVNODE_RE.match(l)]
        self.assertTrue(nodes, msg="no Tegra serial device node present: %s" % output)

    def test_serial_getty_enabled(self):
        status, output = self.target.run("cat /proc/consoles")
        self.assertEqual(status, 0, msg="could not read /proc/consoles: %s" % output)
        self.assertTrue(_CONSOLE_RE.search(output),
                        msg="no Tegra serial console in /proc/consoles: %s" % output)
        devs = [line.split()[0] for line in output.splitlines()
                if _CONSOLE_RE.match(line)]
        for dev in devs:
            status, state = self.target.run(
                "systemctl is-enabled serial-getty@%s.service" % dev)
            if status == 0 or state.strip() in ("enabled", "static", "alias", "indirect"):
                return
        self.fail(
            "no serial-getty enabled for Tegra console(s) %s" % ", ".join(devs))
