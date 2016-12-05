#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class DpkgFinal:
    """Reinstall"""

    def run(self):
        return trigger_reinstall()

class ConfigureAll:
    """rerun dpkg configuration"""
    def run(self):
        shell("dpkg --configure -a")

class ReinstallHalfInstalled:
    """reinstall half-installed packages"""
    def run(self):
        # dpkg -l 'ih' means: Desired=Installed, Status=Half-inst
        packages = shell("dpkg -l|grep -E ^ih|awk '{print $2}'").strip().split("\n")
        for pkg in packages:
           shell("apt-get install -y --allow-unauthenticated --reinstall %s" % (pkg,), timeout=60)

class DpkgCompleted (module.BasicModule):
    """dpkg is in a valid state"""

    repairs = [ConfigureAll(), ReinstallHalfInstalled()]
    final   = DpkgFinal()

    def run(self):
        # identify not completely installed packages in dpkg
        status = shell("dpkg -l|grep -E ^i|grep -vE ^ii")
        if status:
            return False
        return True

register.put(DpkgCompleted())
