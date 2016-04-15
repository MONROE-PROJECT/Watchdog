#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot
from time import time

class TimeFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance()

class RestartNTP():
    """restart ntp service"""
    def run(self):
        shell("systemctl start ntp")

class SystemTime (module.BasicModule):
    """ntp is connected and working"""

    repairs = [RestartNTP()]
    final   = TimeFinal()

    def run(self):
        stratum = shell("ntpq -pn|tail -n4|awk '{print $3}'").split("\n")
        for line in stratum:
            s = int(line)
            if s>0 and s<16:
                return True
        return False

register.put(SystemTime())
