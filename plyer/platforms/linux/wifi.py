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
from subprocess import Popen, PIPE, call, STDOUT


class LinuxWifi(Wifi):
    names = {}

    def _is_enabled(self):
        '''
        Returns `True` if wifi is enabled else `False`.
        '''
        enbl = Popen(["nmcli", "radio", "wifi"], stdout=PIPE, stderr=PIPE)
        if enbl.communicate()[0].split()[0] == "enabled":
            return True
        return False

    def _start_scanning(self):
        '''
        Returns all the network information.
        '''
        if self._is_enabled():
            list_ = wifi.Cell.all('wlan0')
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
        try:
            call(['nmcli', 'nm', 'enable', 'true'])
        finally:
            password = parameters['password']
            cell = self.names[network]
            return wifi.Scheme.for_cell('wlan0', network, cell, password)

    def _disconnect(self):
        '''
        Disconnect all the networks managed by Network manager.
        '''
        return call(['nmcli', 'nm', 'enable', 'false'])


def instance():
    import sys
    try:
        import wifi
        return LinuxWifi()
    except ImportError:
        sys.stderr.write("python-wifi not installed. try:"
                         "`pip install --user wifi`.")

    return Wifi()
