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
    '''
    .. versionadded:: 1.2.5
    '''

    def __init__(self, *args, **kwargs):
        '''
        .. versionadded:: 1.3.3
        '''

        super(LinuxWifi, self).__init__(*args, **kwargs)
        self.names = {}

    @property
    def interfaces(self):
        '''
        .. versionadded:: 1.3.3
        '''

        proc = Popen([
            'nmcli', '--terse',
            '--fields', 'DEVICE,TYPE',
            'device'
        ], stdout=PIPE)
        lines = proc.communicate()[0].decode('utf-8').splitlines()

        interfaces = []
        for line in lines:
            device, dtype = line.split(':')
            if dtype != 'wifi':
                continue
            interfaces.append(device)

        return interfaces

    def _is_enabled(self):
        '''
        Returns `True` if wifi is enabled else `False`.

        .. versionadded:: 1.2.5
        .. versionchanged:: 1.3.2
            nmcli output is properly decoded to unicode
        '''
        enbl = Popen(["nmcli", "radio", "wifi"], stdout=PIPE, stderr=PIPE)
        if enbl.communicate()[0].split()[0].decode('utf-8') == "enabled":
            return True
        return False

    def _start_scanning(self, interface=None):
        '''
        Returns all the network information.

        .. versionadded:: 1.2.5
        .. versionchanged:: 1.3.0
            scan only if wifi is enabled
        '''

        if not interface:
            interface = self.interfaces[0]

        import wifi
        if self._is_enabled():
            list_ = list(wifi.Cell.all(interface))
            for i in range(len(list_)):
                self.names[list_[i].ssid] = list_[i]
        else:
            raise Exception('Wifi not enabled.')

    def _get_network_info(self, name):
        '''
        Starts scanning for available Wi-Fi networks and returns the available,
        devices.

        .. versionadded:: 1.2.5
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

        .. versionadded:: 1.2.5
        '''
        return self.names.keys()

    def _connect(self, network, parameters, interface=None):
        '''
        Expects 2 parameters:
            - name/ssid of the network.
            - parameters:
                - password: dict type

        .. versionadded:: 1.2.5
        '''
        if not interface:
            interface = self.interfaces[0]

        import wifi
        result = None
        try:
            self._enable()
        finally:
            password = parameters['password']
            cell = self.names[network]
            result = wifi.Scheme.for_cell(
                interface, network, cell, password
            )
        return result

    def _disconnect(self, interface=None):
        '''
        Disconnect all the networks managed by Network manager.

        .. versionadded:: 1.2.5
        '''
        if not interface:
            interface = self.interfaces[0]

        if self._nmcli_version() >= (1, 2, 6):
            call(['nmcli', 'dev', 'disconnect', interface])
        else:
            call(['nmcli', 'nm', 'enable', 'false'])

    def _enable(self):
        '''
        Wifi interface power state is set to "ON".

        .. versionadded:: 1.3.2
        '''
        return call(['nmcli', 'radio', 'wifi', 'on'])

    def _disable(self):
        '''
        Wifi interface power state is set to "OFF".

        .. versionadded:: 1.3.2
        '''
        return call(['nmcli', 'radio', 'wifi', 'off'])

    def _nmcli_version(self):
        '''
        .. versionadded:: 1.3.2
        '''
        version = Popen(['nmcli', '-v'], stdout=PIPE)
        version = version.communicate()[0].decode('utf-8')
        while version and not version[0].isdigit():
            version = version[1:]
        return tuple(map(int, (version.split('.'))))


def instance():
    import sys

    try:
        import wifi  # pylint: disable=unused-variable,unused-import
    except ImportError:
        sys.stderr.write("python-wifi not installed. try:"
                         "`pip install --user wifi`.")
        return Wifi()
    return LinuxWifi()
