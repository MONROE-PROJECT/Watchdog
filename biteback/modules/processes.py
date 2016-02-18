#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class ProcessesFinal:
    """Reboot"""
    # the most reliable way to mediate fork bombs
    # smarter fixes should be set in limits.conf

    def run(self):
        return trigger_reboot()

class Processes(module.BasicModule):
    """Open processes"""
    # should be limited by container setup as well

    repairs = []
    final   = ProcessesFinal()

    def run(self):
        pcount = int(shell("ps -AL --no-headers|wc -l"))
        if pcount > 5000:
            return False
        return True

register.put(Processes())
