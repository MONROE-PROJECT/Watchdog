#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance

class ThinpoolFinal:
    """Maintenance"""

    def run(self):
        return trigger_maintenance("Thinpool device out of sync. Unable to remove (check dmsetup ls --tree).")

class RemoveThinpool:
    """remove thinpool device and stop docker daemon"""

    def run(self):
        shell("systemctl stop docker", timeout=60)                                       # should be stopped, just in case 
        shell("dmsetup ls|grep docker-|cut -f1 -d'('|sort|xargs dmsetup remove", timeout=60)  # remove any stale leases on the thinpool
        shell("lvremove -f /dev/mapper/vg--monroe-tp--docker", timeout=60)               # remove the thinpool device
        shell("systemctl start docker")                                                  # will fail, but remove the systemctl status message this test triggers on

class Thinpool (module.BasicModule):
    """docker can access thinpool device"""

    repairs = [RemoveThinpool()]
    final   = ThinpoolFinal()

    def run(self):
        status = shell("systemctl status docker -l")
        if "Unable to take ownership of thin-pool" in status:
            return False
        if "Possibly using a different" in status:  #...thin pool than last invocation
            return False
        if "Base Device UUID and Filesystem verification failed" in status:
            return False
        return True

register.put(Thinpool())
