#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reinstall

class AnsibleFinal:
    """Reinstall"""

    def run(self):
        return trigger_reinstall()

class RescheduleAnsible:
    """restore ansible cron entry"""
    def run(self):
        shell("echo '*/20 * * * * root /usr/bin/ansible-wrapper &>/dev/null' > /etc/cron.d/ansible-wrapper")

class Ansible (module.BasicModule):
    """ansible wrapper installed in crontab"""

    repairs = [RescheduleAnsible()]
    final   = AnsibleFinal()

    def run(self):
        cron =  shell("cat /etc/cron.d/ansible-wrapper")
        if not "/usr/bin/ansible-wrapper" in cron: 
            return False
        return True

register.put(Ansible())
