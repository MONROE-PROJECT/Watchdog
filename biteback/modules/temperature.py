#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class TempFinal:
    """Temporary Maintenance"""

    def run(self):
        return trigger_maintenance()

class Temperature(module.BasicModule):
    """CPU Temperature"""

    repairs = []
    final   = TempFinal()

    def run(self):
        temp = float(shell("/etc/munin/plugins/temp").split(" ")[1])
        if temp > 100.0:
            return False
        return True

register.put(Temperature())
