#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class KModFinal:
    """Temporary Maintenance"""

    def run(self):
        return trigger_maintenance("kernel modules k10temp or sp5100_tco not loaded")

class ReloadKernelModules:
    """reload kernel modules"""

    def run(self):
        shell("depmod")
        shell("modprobe k10temp sp5100_tco")
        shell("systemctl start watchdog")

class KernelModules(module.BasicModule):
    """Check for watchdog and temperature kernel modules"""

    repairs = [ReloadKernelModules()]
    final   = KModFinal()

    def run(self):
        mod = shell("lsmod")
        if not "k10temp" in mod:
            return False
        return True

register.put(KernelModules())
