#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class MTFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance("metadata-timeloop is not running.")

class RestartMT:
    """enable & restart metadata-timeloop service"""
    def run(self):
        shell("systemctl enable metadata-timeloop")
        shell("systemctl restart metadata-timeloop")

class MTService (module.BasicModule):
    """metadata-timeloop service"""

    repairs = [RestartMT()]
    final   = MTFinal()

    def run(self):
        status =  shell("systemctl status metadata-timeloop")
        if not "running" in status:
            return False
        return True

register.put(MTService())
