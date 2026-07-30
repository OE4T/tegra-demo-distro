#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import time

from oeqa.runtime.case import OERuntimeTestCase

class TegraKernelModuleTest(OERuntimeTestCase):
    """Unload and reload the ina3221 hwmon module."""

    module = "ina3221"
    HWMON_POLL_TRIES = 5

    def _ina3221_dev(self):
        # the power sensor's i2c bus/address differs per carrier (p3768 vs p3834); find it by binding
        _, dev = self.target.run("ls -d /sys/bus/i2c/drivers/ina3221/*-* 2>/dev/null | head -n 1")
        return dev.strip()

    def _require_ina3221_bound(self):
        # an ina3221 node in the devicetree but no bound i2c device is a probe failure (must fail);
        # no node at all is genuine absence on this SKU (skip)
        i2c_dev = self._ina3221_dev()
        if i2c_dev:
            return i2c_dev
        _, in_dt = self.target.run(
            "grep -ral ina3221 /sys/firmware/devicetree/base 2>/dev/null | head -n 1")
        self.assertFalse(in_dt.strip(),
                         msg="ina3221 in the devicetree but no bound i2c device; driver probe failed")
        self.skipTest("ina3221 absent from the devicetree on this SKU (no power sensor)")

    def test_unload_reload(self):
        status, fname = self.target.run("modinfo -F filename %s" % self.module)
        if status != 0:
            self.fail("module %s not found by modinfo (image/packaging gap)" % self.module)
        if "builtin" in fname.strip().lower():
            self.skipTest("module %s is built-in, not unloadable" % self.module)

        status, output = self.target.run("modprobe %s" % self.module)
        self.assertEqual(status, 0, msg="initial load failed: %s" % output)

        # ina3221 is DT-bound so refcnt >= 1 at boot; unbind before modprobe -r.
        i2c_dev = self._require_ina3221_bound()

        devname = i2c_dev.split("/")[-1]
        status, out = self.target.run(
            "echo '%s' > /sys/bus/i2c/drivers/%s/unbind" % (devname, self.module))
        self.assertEqual(status, 0,
                         msg="sysfs unbind of %s failed (needed before modprobe -r): %s"
                         % (devname, out))

        status, output = self.target.run("modprobe -r %s" % self.module)
        self.assertEqual(status, 0, msg="unload failed: %s" % output)

        status, output = self.target.run("modprobe %s" % self.module)
        self.assertEqual(status, 0, msg="reload failed: %s" % output)

        status, output = self.target.run("lsmod | grep -w %s" % self.module)
        self.assertEqual(status, 0, msg="module absent after reload: %s" % output)

        status, refcnt = self.target.run(
            "awk '$1==\"%s\"{print $3}' /proc/modules" % self.module)
        self.assertEqual(status, 0, msg=refcnt)
        self.assertRegex(refcnt.strip(), r"^\d+$", msg="bad refcnt: %s" % refcnt)

    def test_hwmon_readable(self):
        i2c_dev = self._require_ina3221_bound()

        status, _ = self.target.run("test -L %s/driver" % i2c_dev)
        self.assertEqual(status, 0,
                         msg="ina3221 driver not bound: %s/driver missing" % i2c_dev)

        # the hwmon channel can re-register asynchronously, so poll briefly
        voltage = ""
        for _ in range(self.HWMON_POLL_TRIES):
            _, voltage = self.target.run("cat %s/hwmon/hwmon*/in1_input 2>/dev/null" % i2c_dev)
            if voltage.strip().isdigit():
                break
            time.sleep(1)
        self.assertRegex(voltage.strip(), r"^\d+$",
                         msg="ina3221 in1_input not a live reading: %r" % voltage)
