#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance, leds
import time

class HubFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance("no mifis found")

class FixHubAuthorized:
    """reset authorized flag"""
    def run(self):
        authfile = shell('for i in $(find /sys -name authorized); do echo -n "$i  "; cat $(echo $i|sed -e "s/authorized/idProduct/"); done | grep 2514 | sed -e "s/ .*//g"', bashEscape=True)
        if authfile and not "no such file" in authfile:
            shell("echo 0 > %s" % authfile, bashEscape=True)
            shell("echo 1 > %s" % authfile, bashEscape=True)

class RebootOnce:
    """reboot once"""
    #TODO: use regular trigger_reboot
    def run(self):
        oncefile = shell("cat /.rebooted")
        if "1" in oncefile:
            return False
        shell("echo 1 > /.rebooted")
        shell("reboot")

class Hub (module.BasicModule):
    """Check if the entire yepkit hub has crashed"""

    repairs = [RebootOnce()]
    final   = HubFinal()

    def run(self):
        links = shell("ip link")
        now = int(time.time())
        if ("usb0" in links) or ("usb1" in links) or ("usb2" in links):
            shell("echo %i > /tmp/last_seen_mifis" % now)
            return True
        last = shell("cat /tmp/last_seen_mifis")
        if "No such file" in last:
            # after reboot, the file does not exist.
            # In that case, we reset the timer and wait for the regular timeout.
            shell("echo %i > /tmp/last_seen_mifis" % now)
        else:
            last = int(last)
            if (now-last) > 1800:
                return False
        return True

register.put(Hub())
