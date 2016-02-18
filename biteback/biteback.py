#!/usr/bin/env python

import sys
import argparse
import register
from util import shell
from modules import *

import zmq
import fileinput

SYSEVENT_FAILED   = "Watchdog.Failed"
SYSEVENT_REPAIRED = "Watchdog.Repaired"
SYSEVENT_STATUS   = "Watchdog.Status"

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


def watchdog(doRepairs=True, doFinals=True):
    print "Imported %i tests" % len(tests)

    success = len(tests)
    run     = 0
    for test in tests:
        print "Running %s" % test.__doc__
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-R","--skip-repairs", help="do not run repair actions", action="store_true")
    parser.add_argument("-F","--skip-finals", help="do not run final actions", action="store_true")
    args = parser.parse_args()

    watchdog(not args.skip_repairs, not args.skip_finals)

if __name__ == "__main__":
    main()
