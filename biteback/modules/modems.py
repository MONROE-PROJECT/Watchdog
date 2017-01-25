#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance, leds
import time

class ModemsFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance("No modems detected")

class Modems (module.BasicModule):
    """Check if we have any modems in the node"""

    repairs = []
    final   = ModemsFinal()

    def run(self):
        modems = shell("modems | jq length")
        if int(modems)==0:
            return False
        return True

register.put(Modems())
