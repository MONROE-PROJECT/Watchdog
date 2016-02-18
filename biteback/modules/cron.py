#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class CronFinal:
    """Reboot"""

    def run(self):
        return trigger_reboot()

class RestartCron:
    """enable & restart cron service"""
    def run(self):
        shell("systemctl enable cron")
        shell("systemctl restart cron")

class CronService (module.BasicModule):
    """cron service"""

    repairs = [RestartCron()]
    final   = CronFinal()

    def run(self):
        ps =  shell("ps ax|grep cron")
        if not "sbin/cron" in ps: 
            return False
        return True

register.put(CronService())
