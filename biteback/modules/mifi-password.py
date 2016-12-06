#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_maintenance
import simplejson as json
import time

class MifiFinal():
	def run(self):
		return trigger_maintenance("MiFi password could not be changed to default.")

class ResetPasswords():
	"""try to reset mifi passwords to the default"""
	def run(self):
	    wifipass=shell("bash -c 'source /etc/default/network-listener; echo $MF910_WIFI_PASS'") 
	    adminpass=shell("bash -c 'source /etc/default/network-listener; echo $MF910_ADMIN_PASS'") 
		
	    if not wifipass or not adminpass:
	        print "No default passwords defined in /etc/default/network-listener"
		return False
			
            pid = shell("pgrep network-listen")
            shell("kill -STOP %s" % pid) 
            time.sleep(300)
            for interface in ["usb0", "usb1", "usb2"]:
                shell("mf910-password %s %s %s" % (interface, wifipass, adminpass))
            shell("rm /var/log/network-listener.log")
            shell("kill -CONT %s" % pid)


class MifiPassword (module.BasicModule):
    """Check if a mifi does not use the default password"""

    repairs = [ResetPasswords() ]
    final   = MifiFinal()

    def run(self):
        logfile = shell("tail -n 20 /var/log/network-listener.log")
        if "LOGIN" in logfile and '"result":"1"' in logfile:
        	return False
        return True
        
        

register.put(MifiPassword())
