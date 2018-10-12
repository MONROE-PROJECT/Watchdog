#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class TempFinal:
    """Temporary Maintenance"""

    def run(self):
        return trigger_maintenance("cpu temperature exceeded")

class Temperature(module.BasicModule):
    """CPU Temperature"""

    repairs = []
    final   = TempFinal()

    def run(self):
        temp = shell("/etc/munin/plugins/temp").split(" ")[1]
        if len(temp) > 0 and temp[0].isdigit():
            # only convert if temp has at least a digit
            temp = float(shell("/etc/munin/plugins/temp").split(" ")[1])
            if temp > 100.0:
                return False 
        
        # for vm environments without sensors, temp is empty/non-digit so return True for these cases.  
        return True

register.put(Temperature())
