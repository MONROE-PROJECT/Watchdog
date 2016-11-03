#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance
import simplejson as json

class MifiFinal:
    """Ignore""" 

    def run(self):
        return None

class RestartMifi:
    """send usbrestart commmand to mifi"""
    def run(self):
        # currently taken care of during the test
        pass

class Mifi (module.BasicModule):
    """Check if the mifis pass curl requests, iff connected"""

    repairs = []
    final   = MifiFinal()

    def run(self):
        modems = json.loads(shell("curl -s http://localhost:88/modems"))
        for modem in modems:
            if modem.get('mode') in ['LTE','4G','UMTS']:
                interface=modem.get('ifname')
                ip4table=modem.get('ip4table')
                code = shell('curl -4 --interface '+interface+' -sL -w "%{http_code}" http://193.10.227.25/test/1000M.zip -r 0-0 -o /dev/null --connect-timeout 10 -m 20; echo " $?"', timeout=30).strip()
                if code=='000 28': # curl failed with a connection timeout
                    #shell('curl -s -X POST http://localhost:88/modems/' + str(ip4table) + '/usbrestart')
                    return False
        return True

register.put(Mifi())
