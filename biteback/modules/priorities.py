#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance
import sqlite3 as db
import simplejson as json

class PrioritiesFinal:
    """Maintenance"""
    def run(self):
        return trigger_maintenance()

class Priorities(module.BasicModule):
    """Correct priorities are set for load balancer interfaces"""

    repairs = []
    final   = PrioritiesFinal()

    # from dlb/Address.h
    PRIO_04MB   = 2
    PRIO_100MB  = 11
    PRIO_500MB  = 13
    PRIO_1000MB = 14

    def run(self):
        conn = db.connect('/etc/config/celerway.db')
        c = conn.cursor()
        links = c.execute("SELECT ICCIDMAC, USEREST from Links")
        links = links.fetchall()

        data = json.loads(shell("curl -s http://localhost:88/dlb"))
        
        priorities = {}
        eth0 = [x['mac'] for x in data['interfaces'] if x['name']=='eth0']
        if eth0:
            priorities[eth0[0]] = self.PRIO_1000MB
        wlan0 = [x['mac'] for x in data['interfaces'] if x['name']=='wlan0']
        if wlan0:
            priorities[wlan0[0]] = self.PRIO_500MB
        wwan0 = [x['iccid'] for x in data['interfaces'] if x['name']=='wwan0']
        if wwan0:
            priorities[wwan0[0]] = self.PRIO_100MB

        for mac,userest in links:
            if mac in priorities:
                if userest != priorities[mac]:
                    c.execute("UPDATE Links SET USEREST=? WHERE ICCIDMAC=?", (priorities[mac], mac))
                    print "Setting %s to %s" % (mac, priorities[mac])
            elif userest != self.PRIO_04MB:
                c.execute("UPDATE Links SET USEREST=? WHERE ICCIDMAC=?", (self.PRIO_04MB, mac))
                print "Setting %s to %s" % (mac, self.PRIO_04MB)
        conn.commit()
        conn.close()
        return True

register.put(Priorities())
