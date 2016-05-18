#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

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

    repairs = [RestartME(), ReinstallME()]
    final   = MEFinal()

    def run(self):
        ps =  shell("ps ax|grep exporter")
        if not "metadata-exporter" in ps: 
            return False
        # is it a service? 
        status =  shell("systemctl status metadata-exporter")
        if not "running" in status: 
            return False
        return True

register.put(MEService())
