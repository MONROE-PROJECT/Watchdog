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
        packages = shell("grep -B1 half-installed /var/lib/dpkg/status").strip().split("\n")
        while len(packages)>1:
           packages.pop()
           pkg = packages.pop().split(":")[1].strip()
           shell("apt-get install -y --allow-unauthenticated --reinstall %s" % (pkg,), timeout=60)

class DpkgCompleted (module.BasicModule):
    """dpkg is in a valid state"""

    repairs = [ConfigureAll(), ReinstallHalfInstalled()]
    final   = DpkgFinal()

    def run(self):
        # identify half-installed and half-configured packages in dpkg
        status = shell("grep half- /var/lib/dpkg/status") 
        if "Status:" in status: 
            return False
        return True

register.put(DpkgCompleted())
