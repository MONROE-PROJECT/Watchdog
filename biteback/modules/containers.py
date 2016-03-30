#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class PullContainers:
    """pull monroe base image and experiments"""
    def run(self):
        shell("docker pull monroe/base")
        #shell("docker pull monroe/ping")
        #...

class DockerExperiments (module.BasicModule):
    """docker (if installed) contains all monroe base containers"""

    repairs = [PullContainers()]
    final   = None

    def run(self):
        # only run these tests if docker is installed
        docker =  shell("docker --version")
        if not "1.10" in docker: 
            return True
 
        images =  shell("docker images")
        if not "monroe/base" in images:
            return False
        return True

register.put(DockerExperiments())
