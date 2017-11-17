#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance
import time
import zmq

class MEFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance("cannot communicate with metadata-exporter")

class ReloadFirewall:
    """reload firewall rules"""
    def run(self):
        shell("circle restart")

class RestartME:
    """enable & restart metadata-exporter service"""
    def run(self):
        shell("systemctl enable metadata-exporter")
        shell("systemctl restart metadata-exporter")

class ReinstallME:
    """reinstall metadata-exporter service"""

    def run(self):
        shell("apt-get install -y --force-yes --reinstall metadata-exporter", timeout=60)

class MEService (module.BasicModule):
    """metadata-exporter service"""

    repairs = [ReloadFirewall(), RestartME()]
    final   = MEFinal()

    def run(self):
        # if the metadata interface does not exist, not connecting is ok
        metadata = shell("ifconfig metadata 2>/dev/null | grep inet | grep ask")
        if not "inet" in metadata:
            return True

        ps =  shell("ps ax|grep exporter")
        if not "metadata-exporter" in ps: 
            return False
        # is it a service? 
        status =  shell("systemctl status metadata-exporter")
        if not "running" in status: 
            return False


        print("Subscribing to ZMQ socket on tcp://172.17.0.1:5556")
        context = zmq.Context()

        sub = context.socket(zmq.SUB)
        sub.connect("tcp://172.17.0.1:5556")
        sub.setsockopt(zmq.SUBSCRIBE, '')

        poller = zmq.Poller()
        poller.register(sub, zmq.POLLIN)

        socks = dict(poller.poll(60000))
        if socks:
            if socks.get(sub) == zmq.POLLIN:
                return True
        else:
            print("Timeout.")
        return False

register.put(MEService())
