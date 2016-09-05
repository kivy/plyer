from plyer.facades import Wifi
from subprocess import Popen, PIPE, call, STDOUT

try:
    import wifi
except ImportError:
    sys.stderr.write("python-wifi not installed. try:"
                     "`sudo pip install wifi`.")
    return Wifi()


class LinuxWifi(Wifi):
    names = {}

    def _is_enabled():
        '''
        TODO: Implement this in future.
        '''
        return

    def _start_scanning(self):
        '''
        Returns all the network information.
        '''
        list_ = wifi.Cell.all('wlan0')
        for i in range(len(list_)):
            self.names[list_[i].ssid] = list_[i]

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
    return LinuxWifi()
