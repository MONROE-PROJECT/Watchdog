#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot
from time import time

class TimeFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance()

class FixTimeSkew:
    """stop ntp service and run ntpd -gq"""
    def run(self):
        shell("systemctl stop ntp")
        shell("ntpd -gq")
        shell("systemctl start ntp")

class RestartNTP():
    """restart ntp service"""
    def run(self):
        shell("systemctl start ntp")

class SystemTime (module.BasicModule):
    """time skew within SSL bounds"""

    repairs = [FixTimeSkew(), RestartNTP()]
    final   = TimeFinal()

    def run(self):
        try:
            offsets = shell("ntpq -pn|awk '{print $9}'|tail -n+3").strip().split("\n")
            for o in offsets:
                if abs(float(o)) > 60:
                    return False
        except:
            try:
                t = int(shell("curl -s www.timeapi.org/utc/now?format=%25s"))
                if abs(time()-t) > 60:
                    return False
            except: # we might just not have connectivity
                pass 
        return True

register.put(SystemTime())
