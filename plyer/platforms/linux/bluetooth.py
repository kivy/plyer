import time
import pexpect
import subprocess
import sys
from plyer.facades import Bluetooth


class LinuxBluetooth(Bluetooth):
    names = {}

    def _enable(self):
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("bluetoothctl", echo = False)
    
    def _disable(self):
 	out = subprocess.check_output("rfkill block bluetooth", shell = True)

    def _scan(self):
        """Start bluetooth scanning process."""
        try:
	    self.child.send("scan on" + "\n")
	    time.sleep(0)
	    out = self.child.before.split("\r\n")
	    print(out)
        except:
            return None

    def _visible(self):
        """Make device discoverable."""
        try:
	    self.child.send("discoverable on" + "\n")
	    time.sleep(2)
	    out = self.child.before.split("\r\n")
  	    print(out)
        except:
            return None

    def _get_scan_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
	try:
	    self.child.send("devices" + "\n")
            time.sleep(pause)
            out = self.child.before.split("\r\n")
	    print(out)
        except:
            return None
        else:
            available_devices = []
            for line in out:
		device = []
        	block_list = ["[\x1b[0;", "removed"]
        	string_valid = not any(keyword in line for keyword in block_list)

        	if string_valid:
            	    try:
                	device_position = line.index("Device")
               	    except ValueError:
                    	pass
            	    else:
                	if device_position > -1:
                            attribute_list = line[device_position:].split(" ", 2)
			    print(device)
		            device = [attribute_list[2], attribute_list[1]]
			    print(device)
                            if device:
                    	        available_devices.append(device)
	    		    if device not in self.names:
		    		self.names.append(device)	
	    return available_devices

    def _get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        try:
	    self.child.send("paired-devices" + "\n")
            time.sleep(pause)
            out = self.child.before.split("\r\n")
            paired_devices = []
            for line in out:
                device = []
        	block_list = ["[\x1b[0;", "removed"]
       		string_valid = not any(keyword in line for keyword in block_list)

        	if string_valid:
            	    try:
                        device_position = line.index("Device")
                    except ValueError:
                	pass
                    else:
                        if device_position > -1:
                	    attribute_list = line[device_position:].split(" ", 2)
		            device = [attribute_list[2], attribute_list[1]]
			    print(device)
                	    if device:
                                paired_devices.append(device)
			    if device not in self.names:
		                self.names.append(device)
	    return paired_devices
	except:
	    return None

    def _pair(self, name):
        """Try to pair with a device by mac address."""
        all_devices = self.names
        try:
	    x = [x for x in all_devices if name in x[0]]
	    mac_address = x[0][1]
	    self.child.send("pair " + mac_address + "\n")
            time.sleep(4)
            out = self.child.before.split("\r\n")
	    print(out)
        except:
            return None

    def _connect(self, name):
        """Try to connect to a device by mac address."""
	all_devices = self.names
        try:
	    x = [x for x in all_devices if name in x[0]]
	    mac_address = x[0][1]
            self.child.send("connect " + mac_address + "\n")
            time.sleep(2)
            out = self.child.before.split("\r\n")
	    print(out, mac_address)
        except:
            return None

    def _disconnect(self, name):
        """Try to disconnect to a device by mac address."""
	all_devices = self.names
        try:
	    x = [x for x in all_devices if name in x[0]]
	    mac_address = x[0][1]
	    self.child.send("disconnect " + mac_address + "\n")
            time.sleep(2)          
            out = self.child.before.split("\r\n")
	    print(out, mac_address)
        except:
            return None
        else:
            res = self.child.expect(["Failed to disconnect", "Successful disconnected", pexpect.EOF])
            success = True if res == 1 else False


def instance(): 
    return LinuxBluetooth()

'''
    def _get_output(self, command, pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
        
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])
	
        if start_failed:
            return None
        
        return self.child.before.split("\r\n")

    def _get_mac(self, name):
	all_devices = self.names
        try:
	    x = [x for x in all_devices if name in x[0]]
	    mac_address = x[0][1]
	    return mac_address
	except:
	    return None
'''
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
'''
    def _parse_device_info(self, info_string):
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
                    r"""device = {
                        "mac_address": attribute_list[1],
                        "name": attribute_list[2]
                    }"""
		    device = [attribute_list[2], attribute_list[1]]

        return names = device
'''


