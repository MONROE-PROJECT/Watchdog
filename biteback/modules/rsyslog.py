#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class RSyslogFinal:
    """Ignore"""

    def run(self):
        pass

class RestartRSyslog:
    """enable & restart rsyslog service"""
    def run(self):
        shell("systemctl enable rsyslog")
        shell("systemctl restart rsyslog")

class RSyslogService (module.BasicModule):
    """rsyslog service"""

    repairs = [RestartRSyslog()]
    final   = RSyslogFinal()

    def run(self):
        ps =  shell("ps ax|grep rsyslog")
        if not "sbin/rsyslog" in ps: 
            return False
        return True

register.put(RSyslogService())
