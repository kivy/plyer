from subprocess import Popen, PIPE
from plyer.facades import Bluetooth
from plyer.utils import whereis_exe
import subprocess
from os import environ


class LinuxBluetooth(Bluetooth):

    def _start(self):
        subprocess.Popen(["service", "bluetooth", "start"])

    def _stop(self):
        subprocess.Popen(["service", "bluetooth", "stop"])


def instance():
    import sys
    if whereis_exe('bluetoothctl'):
        return LinuxBluetooth()
    sys.stderr.write("bluetoothctl not found.")
    return Bluetooth()
