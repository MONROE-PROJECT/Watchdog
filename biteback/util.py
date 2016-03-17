#!/usr/bin/env

import sys
from subprocess import STDOUT, check_output, CalledProcessError

leds_enabled = False

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

def init_leds():
    global leds_enabled
    ok = shell("modprobe leds-apu ledtrig_heartbeat; echo $?").strip()
    if ok == "0":
        leds_enabled = True

def leds(a,b,c):
    global leds_enabled
    if not leds_enabled: return
    if a is not None:
        shell("echo none > /sys/class/leds/apu\:%i/trigger" % (1,))
        shell("echo %i > /sys/class/leds/apu\:%i/brightness" % (1 if a else 0, 1))
    if b is not None:
        shell("echo none > /sys/class/leds/apu\:%i/trigger" % (2,))
        shell("echo %i > /sys/class/leds/apu\:%i/brightness" % (1 if b else 0, 2))
    if c is not None:
        shell("echo none > /sys/class/leds/apu\:%i/trigger" % (3,))
        shell("echo %i > /sys/class/leds/apu\:%i/brightness" % (1 if c else 0, 3))

def led_heartbeat(led):
    global leds_enabled
    if not leds_enabled: return
    shell("echo heartbeat > /sys/class/leds/apu\:%i/trigger" % (led,))
