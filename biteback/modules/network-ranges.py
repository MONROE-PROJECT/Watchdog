#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance, leds

class RangesFinal:
    """Ignore. Restarting the modem will take a moment, even if it is fixed."""
    def run(self):
        pass

class AssignNetworkRange:
    """assign network range to mifi"""
    def run(self):
        for id in xrange(0,2):
            ifname = "usb"+str(id)
            target = "192.168."+str(id)
            ip = shell ("ip -f inet -o addr show "+ifname+" 2>/dev/null | sed -e 's|.*inet \\(.*\\)/.*|\\1|g'").strip()
            if ip and not target in ip:
                shell ("zte-iprange "+ifname+" "+target, timeout=20)

class Ranges (module.BasicModule):
    """Check that mifi network range matches interface name"""

    repairs = [AssignNetworkRange()]
    final   = RangesFinal()

    def run(self):
        for id in xrange(0,2):
            ifname = "usb"+str(id)
            target = "192.168."+str(id)
            ip = shell ("ip -f inet -o addr show "+ifname+" 2>/dev/null | sed -e 's|.*inet \\(.*\\)/.*|\\1|g'").strip()
            if ip and not target in ip:
                print "No match:", ip, ifname, "should be:", target
                return False 
        return True

register.put(Ranges())
