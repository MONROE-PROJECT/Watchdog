#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class MultiFinal:
    """Reboot"""

    def run(self):
        return trigger_reboot()

class RestartMulti:
    """enable & restart multi service"""
    def run(self):
        shell("systemctl enable multi")
        shell("systemctl restart multi")

class ReinstallMulti:
    """reinstall multi service"""

    def run(self):
        shell("apt-get install -y --force-yes --reinstall multi-client", timeout=60)

class MultiService (module.BasicModule):
    """multi service"""

    repairs = [RestartMulti(), ReinstallMulti()]
    final   = MultiFinal()

    def run(self):
        # is multi running
        ps =  shell("ps ax|grep multi")
        if not "multi_client" in ps: 
            return False
        # is it a service? 
        status =  shell("systemctl status multi")
        if not "running" in status: 
            return False
        return True

register.put(MultiService())
