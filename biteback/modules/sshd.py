#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class SSHDFinal:
    """Reboot"""

    def run(self):
        return trigger_reboot()

class RestartSSHD:
    """enable & restart sshd service"""
    def run(self):
        shell("systemctl enable sshd")
        shell("systemctl restart sshd")

class SSHDService (module.BasicModule):
    """sshd service"""

    repairs = [RestartSSHD()]
    final   = SSHDFinal()

    def run(self):
        ps =  shell("ps ax|grep sshd")
        if not "sbin/sshd" in ps: 
            return False
        return True

register.put(SSHDService())
