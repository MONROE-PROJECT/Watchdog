#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance, leds

class HubFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance()

class FixHubAuthorized:
    """reset authorized flag"""
    def run(self):
        authfile = shell('for i in $(find /sys -name authorized); do echo -n "$i  "; cat $(echo $i|sed -e "s/authorized/idProduct/"); done | grep 2514 | sed -e "s/ .*//g"', bashEscape=True)
        if authfile and not "no such file" in authfile:
            shell("echo 0 > %s" % authfile, bashEscape=True)
            shell("echo 1 > %s" % authfile, bashEscape=True)

class Hub (module.BasicModule):
    """Check if the entire yepkit hub has crashed"""

    repairs = [FixHubAuthorized()]
    final   = HubFinal()

    def run(self):
        links = shell("ip link")
        if ("usb0" not in links) and ("usb1" not in links) and ("usb2" not in links):
            return False 
        return True

register.put(Hub())
