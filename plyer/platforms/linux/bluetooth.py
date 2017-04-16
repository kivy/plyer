import time
import pexpect
import subprocess
import sys
from plyer.facades import Bluetooth


class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):
        out = subprocess.call(["rfkill", "unblock", "bluetooth"])
        self.child = pexpect.spawn("bluetoothctl", echo=False, timeout=100)

    def disable(self):
        out = subprocess.call(["rfkill", "block", "bluetooth"])

    def get_output(self, command, pause=0):
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])
        return self.child.before.split("\r\n")

    def start_scan(self):
        """Start bluetooth scanning process."""
        out = self.get_output("scan on")

    def make_discoverable(self):
        """Make device discoverable."""
        out = self.get_output("discoverable on")

    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in
            block_list)

        if string_valid:
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ",
                        2)
                    device = [attribute_list[2], attribute_list[1]]
        return device

    def get_available_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        out = self.get_output("devices")
        available_devices = []
        for line in out:
            device = self.parse_device_info(line)
            if device:
                available_devices.append(device)
        return available_devices

    def get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        out = self.get_output("paired-devices")
        paired_devices = []
        for line in out:
            device = self.parse_device_info(line)
            if device:
                paired_devices.append(device)
        return paired_devices

    def pair(self, name):
        """Try to pair with a device by mac address."""
        mac_address = self.get_mac(name)
        out = self.get_output("pair " + mac_address, 3)

    def connect(self, name):
        """Try to connect to a device by mac address."""
        mac_address = self.get_mac(name)
        out = self.get_output("connect " + mac_address, 3)

    def disconnect(self, name):
        """Try to disconnect to a device by mac address."""
        mac_address = self.get_mac(name)
        out = self.get_output("disconnect " + mac_address, 3)

    def get_mac(self, name):
        all_devices = self.get_available_devices()
        x = [x for x in all_devices if name in x[0]]
        mac_address = x[0][1]
        return mac_address


class LinuxBluetooth(Bluetooth):
    names = {}

    def _enable(self):
        self.obj = Bluetoothctl()

    def _disable(self):
        self.obj.disable()

    def _scan(self):
        """Start bluetooth scanning process."""
        self.obj.start_scan()

    def _visible(self):
        """Make device discoverable."""
        self.obj.make_discoverable()

    def _get_scan_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        scanned_devices = self.obj.get_available_devices()
        scanned_devices_list = []
        for y in scanned_devices:
            scanned_devices_list.append(y[0])
        return scanned_devices_list

    def _get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        paired_devices = self.obj.get_paired_devices()
        paired_devices_list = []
        for y in paired_devices:
            paired_devices_list.append(y[0])
        return paired_devices_list

    def _pair(self, name):
        """Try to pair with a device by mac address."""
        self.obj.pair(name=name)

    def _connect(self, name):
        """Try to connect to a device by mac address."""
        self.obj.connect(name=name)

    def _disconnect(self, name):
        """Try to disconnect to a device by mac address."""
        self.obj.disconnect(name=name)


def instance():
    return LinuxBluetooth()
