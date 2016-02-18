#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class HddFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance()

class ClearLogs:
    """delete rotated log files and other suspects"""
    def run(self):
        shell("rm /var/log/*.gz", timeout=60)
        shell("apt-get clean", timeout=120)

class HddUsage (module.BasicModule):
    """Disk space available"""

    repairs = [ClearLogs()]
    final   = HddFinal()

    def run(self):
        hddleft =  int(shell("df / --output=avail|tail -n1"))
        if hddleft < 2000000:
            return False
        return True

register.put(HddUsage())
