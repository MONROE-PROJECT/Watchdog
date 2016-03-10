#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class Wwan0Final:
    """Maintenance"""

    def run(self):
        return trigger_maintenance()

class RestartNL:
    """restart network-listener"""
    def run(self):
        shell("systemctl restart network-listener")

class Wwan0 (module.BasicModule):
    """Confirm internal modem is up and running"""

    repairs = [RestartNL()]
    final   = Wwan0Final()

    def run(self):
        mode = shell("curl -s http://localhost:88/modems|jq '.[]|select(.ifname == \"wwan0\")|.mode'")
        if mode == "null":
            return False
        return True

register.put(Wwan0())
