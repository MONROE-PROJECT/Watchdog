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
            if float(temp) > 100.0:
                return False 
        
        # Temp is either below max threshold, or in a virtual environment (e.g. qemu)
        # without sensors (temp is empty/non-digit). All good.   
        return True

register.put(Temperature())
