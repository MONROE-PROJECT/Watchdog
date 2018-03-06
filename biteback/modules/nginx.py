#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class NginxFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance("Nginx is not running.")

class RestartNginx:
    """enable & restart nginx service"""
    def run(self):
        shell("systemctl enable nginx")
        shell("systemctl restart nginx")

class NginxService (module.BasicModule):
    """nginx service"""

    repairs = [RestartNginx()]
    final   = NginxFinal()

    def run(self):
        status =  shell("systemctl status nginx")
        if not "running" in status:
            return False
        return True

register.put(NginxService())
