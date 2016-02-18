#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class NLFinal:
    """Reboot"""

    def run(self):
        return trigger_reboot()

class RestartNL:
    """enable & restart network-listener service"""
    def run(self):
        shell("systemctl enable network-listener")
        shell("systemctl restart network-listener")

class ReinstallNL:
    """reinstall network-listener service"""

    def run(self):
        shell("apt-get install -y --force-yes --reinstall network-listener", timeout=60)

class NLService (module.BasicModule):
    """network-listener service"""

    repairs = [RestartNL(), ReinstallNL()]
    final   = NLFinal()

    def run(self):
        # is network listener running
        ps =  shell("ps ax|grep listener")
        if not "network-listener" in ps: 
            return False
        # is it a service? 
        status =  shell("systemctl status network-listener")
        if not "running" in status: 
            return False
        return True

register.put(NLService())
