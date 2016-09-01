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

class RmDocker:
    """delete /var/lib/docker and reinstall docker-engine"""
    def run(self):
        shell("docker stop -t 0 $(docker ps -q)", timeout=60)
        shell("systemctl stop docker", timeout=60)
        shell("rm -r /var/lib/docker", timeout=60)
        shell("apt-get remove docker-engine", timeout=120)

class HddUsage (module.BasicModule):
    """Disk space available"""

    repairs = [ClearLogs(), RmDocker()]
    final   = HddFinal()

    def run(self):
        hddleft =  int(shell("df / --output=avail|tail -n1"))
        if hddleft < 500000:
            return False
        return True

register.put(HddUsage())
