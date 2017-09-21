#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance
import time

class DockerFinal:
    """Maintenance"""

    def run(self):
        last = shell("cat /tmp/last_seen_docker")
        if "No such file" in last:
            # after reboot, the file does not exist.
            # In that case, we reset the timer and wait for the regular timeout.
            shell("date +%s > /tmp/last_seen_docker")
        else:
            last = int(last)
            if (int(time.time())-last) > 3600:
                return trigger_maintenance("docker service has not run for 60 minutes.")

class RestartDocker:
    """enable & restart docker service"""
    def run(self):
        shell("docker stop -t 0 $(docker ps -q)")
        shell("systemctl enable docker")
        shell("systemctl restart docker")

class ReinstallDocker:
    """reinstall docker service"""

    def run(self):
        shell("apt-get install -y --force-yes --reinstall docker-engine", timeout=160)

class DockerService (module.BasicModule):
    """docker service"""

# TODO: Repair #1: restore docker.service file which uses /etc/defaults/docker
    repairs = [RestartDocker()]
    final   = DockerFinal()

    def run(self):
        # if docker is not installed, we assume that is intentional
        installed =  shell("dpkg -l|grep docker-engine")
        if not "ii" in installed:
            return True

        ps = shell("ps ax|grep docker")
        if not "--bip" in ps: 
            return False

        status = shell("systemctl status docker")
        if not "active (running)" in status: 
            return False

        addr = shell("ifconfig docker0 2>/dev/null | grep inet | grep ask").strip()
        if addr != "":
            print "Address detected: -%s-" % addr
            shell("date +%s > /tmp/last_seen_docker")
            return True
        return False

register.put(DockerService())
