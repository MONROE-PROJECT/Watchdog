#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class DLBFinal:
    """Reboot"""

    def run(self):
        return trigger_reboot()

class RestartDLB:
    """enable & restart dlb service"""
    def run(self):
        shell("systemctl enable dlb")
        shell("systemctl restart dlb")

class ReinstallDLB:
    """reinstall dlb service"""

    def run(self):
        shell("apt-get install -y --force-yes --reinstall dlb", timeout=60)

class DLBService (module.BasicModule):
    """dlb service"""

    repairs = [RestartDLB(), ReinstallDLB()]
    final   = DLBFinal()

    def run(self):
        # is network listener running
        ps =  shell("ps ax|grep dlb")
        if not "sbin/dlb" in ps: 
            return False
        # is it a service? 
        status =  shell("systemctl status dlb")
        if not "running" in status: 
            return False
        return True

register.put(DLBService())
