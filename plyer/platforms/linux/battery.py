from subprocess import Popen, PIPE
from plyer.facades import Battery
from plyer.utils import whereis_exe

from os import environ


class LinuxBattery(Battery):
    def _get_state(self):
        old_lang = environ.get('LANG')
        environ['LANG'] = 'C'

        status = {"isCharging": None, "percentage": None}

        # We are supporting only one battery now
        dev = "/org/freedesktop/UPower/device/battery_BAT0"
        upower_process = Popen(["upower", "-d", dev],
                stdout=PIPE)
        output = upower_process.communicate()[0]

        environ['LANG'] = old_lang

        if not output:
            return status

        state = percentage = None
        for l in output.splitlines():
            if 'state' in l:
                state = l.rpartition(':')[-1].strip()
            if 'percentage' in l:
                percentage = float(l.rpartition(':')[-1].strip()[:-1])

        if(state):
            status['isCharging'] = state == "charging"

        status['percentage'] = percentage

        return status


def instance():
    import sys
    if whereis_exe('upower'):
        return LinuxBattery()
    sys.stderr.write("upower not found.")
    return Battery()
