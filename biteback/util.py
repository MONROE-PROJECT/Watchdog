#!/usr/bin/env

import os
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
    ## DISABLED until tested
    ## shell("shutdown -r +1 'System self-test unrecoverable. Trying reboot in 1 min.'")
    ## sleep(300) # wait 5 min, then force reboot if we are still running.
    ## shell("echo 1 > /proc/sys/kernel/sysrq")
    ## shell("echo b > /proc/sysrq-trigger")
    pass

def trigger_reinstall():
    # TODO: remove the successful boot hint to cause reinstall 
    # on boot

    ## DISABLED until tested
    ## shell("grub-editenv /.bootos set FORCEREINSTALL=1")
    trigger_reboot()

def shell(cmd, timeout=10, source=None, bashEscape=False):
    if bashEscape:
        cmd = "timeout -s 9 %i bash -c '%s'" % (timeout, cmd)
    else:
        cmd = "timeout -s 9 %i %s" % (timeout, cmd)
    if source:
        cmd = ". %s && %s" % (source, cmd)
    print "Running: %s" % cmd
    try:
      env = os.environ.copy()
      env['PATH']='/usr/bin/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
      output = check_output(cmd, stderr=STDOUT, shell=True, env=env)
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
