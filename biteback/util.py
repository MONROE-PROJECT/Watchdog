#!/usr/bin/env

import sys
from subprocess import STDOUT, check_output, CalledProcessError

def trigger_maintenance():
    # TODO: stop all experiments and set a maintenance flag
    pass

def trigger_reboot():
    # TODO: write a reboot hint to the self-test result file
    # causing the watchdog plugin to return an error code
    # causing the watchdog to reboot the node.
    pass

def trigger_reinstall():
    # TODO: remove the successful boot hint to cause reinstall 
    # on boot
    trigger_reboot()

def shell(cmd, timeout=10, source=None):
    cmd = "timeout -s 9 %i %s" % (timeout, cmd)
    if source:
        cmd = ". %s && %s" % (source, cmd)
    print "Running: %s" % cmd
    try:
      output = check_output(cmd, stderr=STDOUT, shell=True)
    except OSError,er:
      output = str(er)
    except CalledProcessError,er:
      output = er.output
    except Exception,ex:
      print "[DEBUG]", ex
      output = "Failed"
    return output
