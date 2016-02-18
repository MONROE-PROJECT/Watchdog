#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class MuninFinal:
    """Reboot"""

    def run(self):
        return trigger_reboot()

class ReinstallMunin:
    """reinstall munin service"""

    def run(self):
        shell("apt-get install -y --force-yes --reinstall munin-plugins-monroe munin-node-c", timeout=60)

class MuninService (module.BasicModule):
    """munin service"""

    repairs = [ReinstallMunin()]
    final   = MuninFinal()

    def run(self):
        # does the munin server reply
        ps =  shell('echo -e list\\\\nquit\\\\n|nc localhost 4949')
        if not "cpu" in ps: 
            return False
        return True

register.put(MuninService())
