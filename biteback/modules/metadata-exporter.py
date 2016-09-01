#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance
import time
import zmq

class MEFinal:
    """Reboot"""

    def run(self):
        return trigger_maintenance()

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

    repairs = [RestartME()]
    final   = MEFinal()

    def run(self):
        ps =  shell("ps ax|grep exporter")
        if not "metadata-exporter" in ps: 
            return False
        # is it a service? 
        status =  shell("systemctl status metadata-exporter")
        if not "running" in status: 
            return False

        # if the docker0 interface does not exist, not connecting is ok
        docker = shell("ifconfig docker0 2>/dev/null | grep inet | grep ask")
        if not "inet" in docker:
            return True

        print("Subscribing to ZMQ socket on tcp://172.17.0.1:5556")
        context = zmq.Context()

        sub = context.socket(zmq.SUB)
        sub.connect("tcp://172.17.0.1:5556")
        sub.setsockopt(zmq.SUBSCRIBE, '')

        poller = zmq.Poller()
        poller.register(sub, zmq.POLLIN)

        socks = dict(poller.poll(10000))
        if socks:
            if socks.get(sub) == zmq.POLLIN:
                return True
        else:
            print("Timeout.")
        return False

register.put(MEService())
