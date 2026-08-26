#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase

class TegraUsbTest(OERuntimeTestCase):
    """USB root hub enumerated and a downstream device attached."""

    READ_MB = 8

    def test_host_controller(self):
        status, _ = self.target.run("test -d /sys/bus/usb/devices")
        self.assertEqual(status, 0, msg="no USB host support (/sys/bus/usb/devices absent)")
        status, output = self.target.run("ls -d /sys/bus/usb/devices/usb* 2>/dev/null")
        self.assertEqual(status, 0, msg="no USB root hub: %s" % output)
        self.assertRegex(output, r"/usb\d", msg="no USB root hub enumerated: %s" % output)

    def test_downstream_device(self):
        # grep -v ':' drops interface entries (e.g. 1-0:1.0) present even with nothing plugged in
        _, output = self.target.run(
            "ls -d /sys/bus/usb/devices/*-* 2>/dev/null | grep -v ':'")
        # an unoccupied port is a bench fact, not a defect; skip rather than fail
        if not output.strip():
            self.skipTest("no downstream USB device attached")
        self.assertRegex(output, r"devices/\d+-\d", msg="malformed USB device path: %s" % output)

    def test_mass_storage(self):
        # a mass-storage interface (class 08) with no /dev/sd = the driver did not bind
        _, ms = self.target.run(
            "grep -l '^08$' /sys/bus/usb/devices/*/bInterfaceClass 2>/dev/null")
        if not ms.strip():
            self.skipTest("no USB mass-storage device attached")
        _, blk = self.target.run(
            "for b in /sys/block/sd*; do [ -e \"$b\" ] && "
            "readlink -f \"$b\" | grep -q usb && basename \"$b\"; done")
        blk = blk.split()
        self.assertTrue(blk,
                        msg="USB mass-storage device enumerated but no /dev/sd block device; "
                            "usb-storage/uas driver did not bind (image driver gap)")
        dev = "/dev/%s" % blk[0]
        # non-destructive: read a few MB off the raw device to exercise the USB data path
        status, output = self.target.run(
            "dd if=%s of=/dev/null bs=1M count=%d 2>&1" % (dev, self.READ_MB))
        self.assertEqual(status, 0, msg="USB read from %s failed: %s" % (dev, output))
        self.assertRegex(output, r"%d\+0 records (in|out)" % self.READ_MB,
                         msg="USB read moved fewer than %dMB from %s: %s" % (self.READ_MB, dev, output))
