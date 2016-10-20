#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance
import time
import zmq

class MetaFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance("cannot retrieve metadata in monroe netns")

class ResetContainers:
    """stop all containers and restart base experiments"""
    def run(self):
        shell("docker stop -t 0 $(docker ps -q)")
        shell("monroe-experiments")

class Metadata (module.BasicModule):
    """metadata-exporter service"""

    repairs = [ResetContainers()]
    final   = MetaFinal()

    def run(self):
        netns = shell("ip netns list")
        if not "monroe" in netns:
            print "Netns monroe does not exist. Ignoring"
            return True
        metadata = shell("ip netns exec monroe metadata | head -n 1")
        if "MONROE" in metadata:
            return True
        return False

register.put(Metadata())
