from subprocess import Popen, PIPE
from plyer.facades import Battery
from plyer.utils import whereis_exe


class OSXBattery(Battery):
    def _get_state(self):
        status = {"isCharging": None, "percentage": None}

        ioreg_process = Popen(["ioreg", "-rc", "AppleSmartBattery"],
                stdout=PIPE)
        output = ioreg_process.communicate()[0]

        if not output:
            return status

        IsCharging = MaxCapacity = CurrentCapacity = None
        for l in output.splitlines():
            if 'IsCharging' in l:
                IsCharging = l.rpartition('=')[-1].strip()
            if 'MaxCapacity' in l:
                MaxCapacity = float(l.rpartition('=')[-1].strip())
            if 'CurrentCapacity' in l:
                CurrentCapacity = float(l.rpartition('=')[-1].strip())

        if (IsCharging):
            status['isCharging'] = IsCharging == "Yes"

        if (CurrentCapacity and MaxCapacity):
            status['percentage'] = 100. * CurrentCapacity / MaxCapacity

        return status


def instance():
    import sys
    if whereis_exe('ioreg'):
        return OSXBattery()
    sys.stderr.write("ioreg not found.")
    return Battery()
