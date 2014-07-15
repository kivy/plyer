from subprocess import Popen, PIPE
from plyer.facades import Battery
from plyer.utils import whereis_exe


class OSXBattery(Battery):
    def _get_status(self):
        status = {"connected": None, "percentage": None}

        ioreg_process = Popen(["ioreg", "-rc", "AppleSmartBattery"],
                stdout=PIPE)
        output = ioreg_process.communicate()[0]

        if not output:
            return status

        ExternalConnected = MaxCapacity = CurrentCapacity = None
        for l in output.splitlines():
            if 'ExternalConnected' in l:
                ExternalConnected = l.rpartition('=')[-1].strip()
            if 'MaxCapacity' in l:
                MaxCapacity = float(l.rpartition('=')[-1].strip())
            if 'CurrentCapacity' in l:
                CurrentCapacity = float(l.rpartition('=')[-1].strip())

        if (ExternalConnected):
            status['connected'] = ExternalConnected == "Yes"

        if (CurrentCapacity and MaxCapacity):
            status['percentage'] = 100. * CurrentCapacity / MaxCapacity

        return status


def instance():
    import sys
    if whereis_exe('ioreg'):
        return OSXBattery()
    sys.stderr.write("ioreg not found.")
    return Battery()
