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
