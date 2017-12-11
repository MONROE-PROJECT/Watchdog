#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class AtqFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance()

class CleanAtqSpool:
    """clean the atq spool and reboot marvind"""
    def run(self):
        shell("rm /var/spool/cron/atjobs/=*")
        shell("mv /var/log/marvind.log /var/log/marvind.log.atq")
        shell("systemctl restart marvind")

class Atq (module.BasicModule):
    """no jobs are stuck in atq"""

    repairs = [CleanAtqSpool()]
    final   = AtqFinal()

    def run(self):
        running = int(shell("atq | grep = | wc -l"))
        if running > 1:
            return False
        return True

register.put(Atq())
