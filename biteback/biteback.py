#!/usr/bin/env python

import sys
import argparse
import register
from time import time

from util import *
from modules import *

import zmq
import fileinput

SYSEVENT_FAILED   = "Watchdog.Failed"
SYSEVENT_REPAIRED = "Watchdog.Repaired"
SYSEVENT_STATUS   = "Watchdog.Status"

POLICY_RUN_DELAY  = 300

tests = register.get()
context = zmq.Context()

def sysevent(message, eventType = SYSEVENT_FAILED):
    try:
        socket = context.socket(zmq.REQ)
        socket.connect("ipc:///tmp/sysevent")
        socket.send("{\"EventType\": \"%s\", \"message\": \"%s\"}" % (eventType, message))
        socket.close(5) 
    except Exception, ex:
        pass
    print message

def succeeds(method):
    try:
        return method()
    except Exception, ex:
        print "[DEBUG2]",ex
        return False

def watchdog(doRepairs=True, doFinals=True, doForce=False):
    if not doForce:
        lastRun = 0
        try:
            lastRun = int(open("/tmp/biteback.last", "r").read())
        except Exception,ex:
            pass 
    
        delta = time()-lastRun
        if delta < POLICY_RUN_DELAY and delta>=0:
            print "Skipping run. Last run was %i seconds ago." % (delta,)
            sys.exit(0) 

    print "Imported %i tests" % len(tests)

    success = len(tests)
    run     = 0

    # Running tests: One on, one blinking
    leds(True, False, False)
    led_heartbeat(2)
    led_heartbeat(3)

    for test in tests:
        print "Testing %s" % test.__doc__
        if not succeeds(test.run):
            sysevent("Failed %s" % test.__doc__, SYSEVENT_FAILED)
            if not doRepairs: 
                success -= 1
                continue

            for repair in test.get_repairs():
                print "Trying %s" % repair.__doc__
                succeeds(repair.run)
                if succeeds(test.run):
                    sysevent("Fixed using %s" % repair.__doc__, SYSEVENT_REPAIRED)
                    break;
            if not succeeds(test.run):
                success -= 1
                final = test.get_final()
                if not doFinals: continue
                sysevent("Resolving to %s" % final.__doc__, SYSEVENT_FAILED)
                succeeds(final.run)
        run += 1

    sysevent("%i/%i tests succeeded, %i tests run." % (success, len(tests), run), SYSEVENT_STATUS)
    if success == len(tests):
        leds(True, True, True)
    elif success == len(tests)-1 and not succeeds(Hub().run):
        leds(True, True, False)
    else:
        # Failed tests: One green light - the third one will be set if the hub is connected with modems
        leds(True, False, False)
    fd = open("/tmp/biteback.last","w")
    fd.write(str(int(time())))
    fd.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-R","--skip-repairs", help="do not run repair actions", action="store_true")
    parser.add_argument("-F","--skip-finals", help="do not run final actions", action="store_true")
    parser.add_argument("-f","--force", help="run, despite having run during the last %i seconds" % (POLICY_RUN_DELAY,), action="store_true")
    args = parser.parse_args()

    init_leds()
    watchdog(not args.skip_repairs, not args.skip_finals, args.force)

if __name__ == "__main__":
    main()
