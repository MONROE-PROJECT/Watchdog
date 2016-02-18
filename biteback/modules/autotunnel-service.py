#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class AutotunnelFinal:
    """Reboot"""

    def run(self):
        return trigger_reboot()

class RestartTunnel:
    """enable & restart autotunnel service"""
    def run(self):
        shell("systemctl enable autotunnel")
        shell("systemctl restart autotunnel")

class ReinstallTunnel:
    """reinstall autotunnel service"""

    def run(self):
        shell("apt-get install -y --force-yes --reinstall autotunnel")

class AutotunnelService (module.BasicModule):
    """Autotunnel systemd service"""

    repairs = [RestartTunnel(), ReinstallTunnel()]
    final   = AutotunnelFinal()

    def run(self):
        # is the watcher running
        ps =  shell("ps ax|grep autotunnel")
        if not "watcher" in ps:
            return False
        status = shell("systemctl status autotunnel")
        if not "running" in status: 
            return False
        return True

register.put(AutotunnelService())
