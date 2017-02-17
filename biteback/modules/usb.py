#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance
import time

class UsbFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance("Unresolved usb issues")

class RebootOnce:
    """reboot once"""
    #TODO: use regular trigger_reboot
    def run(self):
        now = int(time.time())
        oncefile = shell("cat /.rebooted")
        if not "not found" in oncefile and int(oncefile) > now-86400:
            return False
        shell("date +%s > /.rebooted")
        shell("reboot")

class Usb (module.BasicModule):
    """Check if we have usb errors in dmesg"""

    repairs = [RebootOnce()]
    final   = UsbFinal()

    def run(self):
        dmesg = shell("dmesg|grep usb|tail")
        if "error -" in dmesg:
            return False
        return True

register.put(Usb())
