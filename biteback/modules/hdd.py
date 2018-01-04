#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class HddFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance("less than 500000 bytes of free disk space.")

class ClearLogs:
    """delete rotated log files, tmp files and other suspects"""
    def run(self):
        shell("rm /var/log/*.gz /var/log/*.? /var/tmp/*", timeout=60)
        shell("rm /var/lib/docker/tmp/* || true", timeout=60)
        shell("cd /tmp && ls | grep metadata | grep json | xargs -n 1 rm", timeout=500)
        shell("apt-get -y autoremove", timeout=120)
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

    repairs = [ClearLogs()]
    final   = HddFinal()

    def run(self):
        hddleft =  int(shell("df / --output=avail|tail -n1"))
        if hddleft < 500000:
            return False
        hddleft =  int(shell("df /tmp --output=avail|tail -n1"))
        if hddleft < 10000:
            return False
        hddleft =  int(shell("df /var/log --output=avail|tail -n1"))
        if hddleft < 10000:
            return False
        return True

register.put(HddUsage())
