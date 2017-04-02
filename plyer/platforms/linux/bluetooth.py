import time
import pexpect
import subprocess
import sys
from plyer.facades import Bluetooth


class LinuxBluetooth(Bluetooth):

    def _enable(self):
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("bluetoothctl", echo = False)
    
    def _disable(self):
 	out = subprocess.check_output("rfkill block bluetooth", shell = True)

    def get_output(self, command, pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
        
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])
	
        if start_failed:
            return None
        
        return self.child.before.split("\r\n")

    def get_mac(self, name):
	all_devices = self.get_available_devices()
        try:
	    x = [x for x in all_devices if name in x[0]]
	    mac_address = x[0][1]
	    return mac_address
	except:
	    return None

    def _scan(self):
        """Start bluetooth scanning process."""
        try:
            out = self.get_output("scan on")
        except:
            return None

    def _visible(self):
        """Make device discoverable."""
        try:
            out = self.get_output("discoverable on")
        except:
            return None

    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
                    r'''device = {
                        "mac_address": attribute_list[1],
                        "name": attribute_list[2]
                    }'''
		    device = [attribute_list[2], attribute_list[1]]

        return device

    def _get_scan_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        try:
            out = self.get_output("devices")
        except:
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)

            return available_devices

    def _get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        try:
            out = self.get_output("paired-devices")
        except:
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    paired_devices.append(device)
		
            return paired_devices
'''
    def get_discoverable_devices(self):
        """Filter paired devices out of available."""
	available = self.get_available_devices()
        paired = self.get_paired_devices()

        return [d for d in available if d not in paired]
	#all_devices.extend(self.get_available_devices())
	
        self.available_devices = self.get_available_devices()
        self.paired_devices = self.get_paired_devices()
        print(self.paired_devices)
	for i in self.available_devices:
            all_devices.update(i)
        for i in self.paired_devices:
            all_devices.update(i)
        all_devices.update(self.available_devices)
        all_devices.update(self.paired_devices)
        #return [d for d in available if d not in paired]
        return all_devices.values()
'''
'''	
    def get_device_info(self, name):
        """Get device info by mac address."""
        mac_address = self.get_mac(name)
        try:
            out = self.get_output("info " + mac_address)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            return out
'''
    def _pair(self, name):
        """Try to pair with a device by mac address."""
        mac_address = self.get_mac(name)
        try:
            out = self.get_output("pair " + mac_address, 4)
        except:
            return None
'''
    def remove(self, name):
        """Remove paired device by mac address, return success of the operation."""
	mac_address = self.get_mac(name)
        try:
            out = self.get_output("remove " + mac_address, 3)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["not available", "Device has been removed", pexpect.EOF])
            success = True if res == 1 else False
            return success
'''
    def _connect(self, name):
        """Try to connect to a device by mac address."""
	mac_address = self.get_mac(name)
        try:
            out = self.get_output("connect " + mac_address, 2)
        except:
            return None

    def _disconnect(self, name):
        """Try to disconnect to a device by mac address."""
	mac_address = self.get_mac(name)
        try:
            out = self.get_output("disconnect " + mac_address, 2)
        except:
            return None
        else:
            res = self.child.expect(["Failed to disconnect", "Successful disconnected", pexpect.EOF])
            success = True if res == 1 else False


def instance(): 
    return LinuxBluetooth()
