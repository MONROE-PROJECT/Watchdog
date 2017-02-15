#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class AutotunnelFinal:
    """Reinstall if no connection in three days"""

    def run(self):
        last = None
        try:
            last   = int(shell('cat /var/lib/biteback/autotunnel.last'))
        except:
            pass
        if last is None:
            return # Ignore
        uptime = int(shell("tuptime -s --csv --tsince %s | tail -n 1 | cut -d, -f2 | tr -d \\\"" % last)) # uptime since last tunnel
        if uptime > 259200: # three days
            return trigger_reinstall()
        # TODO: how often should we reboot before trying a reinstall?
        #if uptime > 86400:  # one day
        #    return trigger_reboot()

class Autotunnel (module.BasicModule):
    """Backend reachable via autotunnel"""

    repairs = []
    final   = AutotunnelFinal()

    def run(self):
        """check if we can successfully reach the backend"""

        tunnel = shell('ssh -o StrictHostKeychecking=no -i $BACKEND_SSH_KEY -o ConnectTimeout=5 -o BatchMode=yes -o UserKnownHostsFile=/dev/null $BACKEND_SSH_USER@$BACKEND_SSH_SERVER echo success', source='/etc/default/autotunnel')
        if not "success" in tunnel:
            return False

        # store last successful connection in a file
        shell('mkdir -p /var/lib/biteback/')
        shell('date +%s > /var/lib/biteback/autotunnel.last')
        return True

register.put(Autotunnel())
