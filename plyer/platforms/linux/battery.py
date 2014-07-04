from subprocess import Popen, PIPE
from plyer.facades import Battery


class LinuxBattery(Battery):
    def _get_status(self):
        status = {"connected": None, "percentage": None}

        # We are supporting only one battery now
        dev = "/org/freedesktop/UPower/device/battery_BAT0"
        upower_process = Popen(["upower", "-d", dev],
                stdout=PIPE)
        output = upower_process.communicate()[0]

        if not output:
            return status

        power_supply = percentage = None
        for l in output.splitlines():
            if 'power supply' in l:
                power_supply = l.rpartition(':')[-1].strip()
            if 'percentage' in l:
                percentage = float(l.rpartition(':')[-1].strip()[:-1])

        if(power_supply):
            status['connected'] = power_supply == "yes"

        status['percentage'] = percentage

        return status


def instance():
    return LinuxBattery()
