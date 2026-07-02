#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.runtime.decorator.package import OEHasPackage
from oeqa.core.decorator.depends import OETestDepends

class TegraDockerTest(OERuntimeTestCase):
    """docker daemon, the nvidia container runtime, and a GPU workload in a container."""

    @OEHasPackage(["docker-moby"])
    def test_docker_daemon(self):
        status, output = self.target.run("docker info")
        self.assertEqual(status, 0, msg="docker daemon not responsive:\n%s" % output[-2000:])

    @OEHasPackage(["docker-moby"])
    @OETestDepends(['tegra_docker.TegraDockerTest.test_docker_daemon'])
    def test_nvidia_runtime(self):
        for tool in ("nvidia-ctk", "nvidia-container-runtime"):
            self.assertEqual(self.target.run("command -v %s" % tool)[0], 0,
                             msg="%s missing; nvidia-container-toolkit packaging gap" % tool)
        status, out = self.target.run("docker info -f '{{json .Runtimes}}'")
        self.assertIn("nvidia", out,
                      msg="nvidia runtime not registered; check nvidia-container-setup.service:\n%s" % out)

    @OEHasPackage(["nvidia-docker-tests"])
    @OETestDepends(['tegra_docker.TegraDockerTest.test_nvidia_runtime'])
    def test_docker_gpu(self):
        # run-docker-tests pulls and runs the NGC GPU containers; it fails hard when the
        # board cannot reach nvcr.io (the bench is assumed networked, per the suite policy)
        status, output = self.target.run("run-docker-tests", timeout=1800)
        self.assertEqual(status, 0, msg="run-docker-tests failed:\n%s" % output[-2000:])
