#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance
import sqlite3 as db
import simplejson as json
import requests     # this import is slow. 

class PrioritiesFinal:
    """Maintenance"""
    def run(self):
        return trigger_maintenance("(priorities module failed, how?)")

class Priorities(module.BasicModule):
    """Correct priorities are set for load balancer interfaces"""

    repairs = []
    final   = PrioritiesFinal()

    # from dlb/Address.h
    PRIO_04MB = 3
    PRIO_50MB = 11
    PRIO_100MB = 12
    PRIO_500MB  = 14
    PRIO_1000MB = 15

    def run(self):
        dlbdata = requests.get('http://localhost:88/dlb')
        post = []
        for iface in dlbdata.json().get('interfaces'):
            name  = iface.get('name')
            index = iface.get('index')
            iid = iface.get('iccid',iface.get('mac'))
            conn = iface.get('conn')
            if "eth" in name:
                post.append({'mac':iid, 'index':index, 'conn':PRIO_1000MB})
            elif "wlan" in name:
                post.append({'mac':iid, 'index':index, 'conn':PRIO_500MB})
            elif (conn != PRIO_50MB) and (conn != PRIO_04MB):
                # these two values are set by the scheduling client
                post.append({'iccid':iid, 'index':index, 'conn':PRIO_04MB})
        payload = json.dumps({'interfaces':post})
        requests.post('http://localhost:88/dlb', payload)

        return True

register.put(Priorities())
