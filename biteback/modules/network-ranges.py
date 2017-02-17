#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance
from random import randint

class RangesFinal:
    """Ignore. Restarting the modem will take a moment, even if it is fixed."""
    def run(self):
        pass

class AssignNetworkRange:
    """assign network range to mifi"""
    def run(self):
        ranges = []
        for id in xrange(0,3):
            ifname = "usb"+str(id)
            ip = shell ("ip -f inet -o addr show "+ifname+" 2>/dev/null | sed -e 's|.*inet \\(.*\\)\\..*/.*|\\1|g'").strip()
            while ip in ranges:
                target = "192.168."+str(randint(1,250))
                if target in ranges:
                    continue
                shell ("mf910-iprange "+ifname+" "+target, timeout=20)
                ip = target
            ranges.append(ip)

class Ranges (module.BasicModule):
    """Check that mifi network range matches interface name"""

    repairs = [AssignNetworkRange()]
    final   = RangesFinal()

    def run(self):
        ranges = []
        for id in xrange(0,3):
            ifname = "usb"+str(id)
            ip = shell ("ip -f inet -o addr show "+ifname+" 2>/dev/null | sed -e 's|.*inet \\(.*\\)\\..*/.*|\\1|g'").strip()
            if "192" in ip and ip in ranges:
                print "Duplicate IP range: ",ip
                return False
            ranges.append(ip)
        return True

register.put(Ranges())
