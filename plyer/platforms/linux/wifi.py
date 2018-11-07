'''
    Note::
        This facade depends on:
        - nmcli (Network Manager command line tool)
            It is found in most of the popular distros. Support for other
            managers is not provided yet.

        - python-wifi module
            `https://wifi.readthedocs.io/en/latest/`
            `https://github.com/rockymeza/wifi`

'''

from plyer.facades import Wifi
from subprocess import Popen, PIPE, call


class LinuxWifi(Wifi):
    def __init__(self):
        self.ifname = self.getIfname()
        self.nmcliVersion = self.getNmcliVersion()

    names = {}

    def getIfname(self):
        '''
        Return wifi interface name if available else return "wlan0'
        '''
        com = Popen(["nmcli", "-t", "device"], stdout=PIPE)
        com = com.communicate()[0].decode().split("\n")
        for i in com:
            if("wifi" in i):
                return i.split(":")[0]
        return 'wlan0'

    def getNmcliVersion(self):
        '''
        Return nmcli version in Int to perform operation accordingly 
        '''
        com = Popen(["nmcli", "--version"], stdout=PIPE)
        com = com.communicate()[0].decode("utf-8").strip()
        return int(com.split(" ")[-1].replace(".", ""))

    def _is_enabled(self):
        '''
        Returns `True` if wifi is enabled else `False`.
        '''
        enbl = Popen(["nmcli", "radio", "wifi"], stdout=PIPE, stderr=PIPE)
        if enbl.communicate()[0].split()[0].decode('utf-8') == "enabled":
            return True
        return False

    def _start_scanning(self):
        '''
        Returns all the network information.
        '''
        if self._is_enabled():
            list_ = wifi.Cell.all(self.ifname)
            for i in range(len(list_)):
                self.names[list_[i].ssid] = list_[i]
        else:
            raise Exception('Wifi not enabled.')

    def _get_network_info(self, name):
        '''
        Starts scanning for available Wi-Fi networks and returns the available,
        devices.
        '''
        ret_list = {}
        ret_list['ssid'] = self.names[name].ssid
        ret_list['signal'] = self.names[name].signal
        ret_list['quality'] = self.names[name].quality
        ret_list['frequency'] = self.names[name].frequency
        ret_list['bitrates'] = self.names[name].bitrates
        ret_list['encrypted'] = self.names[name].encrypted
        ret_list['channel'] = self.names[name].channel
        ret_list['address'] = self.names[name].address
        ret_list['mode'] = self.names[name].mode
        if not ret_list['encrypted']:
            return ret_list
        else:
            ret_list['encryption_type'] = self.names[name].encryption_type
            return ret_list

    def _get_available_wifi(self):
        '''
        Returns the name of available networks.
        '''
        return self.names.keys()

    def _connect(self, network, parameters):
        '''
        Expects 2 parameters:
            - name/ssid of the network.
            - parameters:
                - password: dict type
        '''

        result = None
        try:
            call(['nmcli', 'nm', 'enable', 'true'])
        finally:
            password = parameters['password']
            cell = self.names[network]
            result = wifi.Scheme.for_cell(
                self.ifname, network, cell, password
            )
        return result

    def _disconnect(self):
        '''
        Disconnect all the networks managed by Network manager.
        '''
        if(self.nmcliVersion > 98):
            return call(['nmcli', 'networking', 'off'])
        else:
            return call(['nmcli', 'nm', 'enable', 'false'])


def instance():
    import sys
    try:
        import wifi  # pylint: disable=unused-variable
        return LinuxWifi()
    except ImportError:
        sys.stderr.write("python-wifi not installed. try:"
                         "`pip install --user wifi`.")

    return Wifi()
