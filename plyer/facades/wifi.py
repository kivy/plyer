'''
Wifi Facade.
=============

The :class:`Wifi` is to provide access to the wifi of your mobile/ desktop
devices.

It currently supports `connecting`, `disconnecting`, `scanning`, `getting
available wifi network list` and `getting network information`.

Simple examples
---------------

To enable/ turn on wifi scanning::

    >>> from plyer import wifi
    >>> wifi.start_scanning()

Once the wifi is enabled/ turned on, then this command starts to scan
all the nearby available wifi networks.

To get network info::

    >>> from plyer import wifi
    >>> wifi.start_scanning()
    >>> return wifi.get_network_info(name)

Returns network details of the network who's name/ssid is provided in the
`name` parameter.

To connect to a network::

    >>> from plyer import wifi
    >>> wifi.start_scanning()
    >>> wifi.connect(network, parameters)

This connects to the network who's name/ssid is provided under `network`
parameter and along with other necessary methods for connection
which depends upon platform to platform.

please visit following files for more details about requirements of
`paramaters` argument in `connect` method:

    plyer/platforms/win/wifi.py
    plyer/platforms/macosx/wifi.py
    plyer/platforms/win/wifi.py

To disconnect from wifi::

    >>> from plyer import wifi
    >>> wifi.disconnect()

This disconnects your device from any wifi network.

To get available wifi networks::

    >>> from plyer import wifi
    >>> wifi.start_scanning()
    >>> return wifi.get_available_wifi()

This returns all the available wifi networks near the device.
'''


class Wifi(object):
    '''Wifi Facade.
    '''

    def is_enabled(self):
        '''
        Returns `True`if the Wifi is enables else `False`.
        '''
        return self._is_enabled()

    def start_scanning(self):
        '''
        Turn on scanning.
        '''
        self._start_scanning()

    def get_network_info(self, name):
        '''
        Return a dictionary of secified network.
        '''
        return self._get_access_points(name=name)

    def get_available_wifi(self):
        '''
        Returns a list of all the available wifi.
        '''
        self._get_available_wifi()

    def connect(self, network, parameters):
        '''
        Method to connect to some network.
        '''
        self._connect(network=network, parameters=parameters)

    def disconnect(self):
        '''
        To disconnect from some network.
        '''
        self._disconnect()

    # private

    def _is_enabled(self):
        raise NotImplementedError()

    def _start_scanning(self):
        raise NotImplementedError()

    def _get_network_info(self, **kwargs):
        raise NotImplementedError()

    def _get_available_wifi(self):
        raise NotImplementedError()

    def _connect(self, **kwargs):
        raise NotImplementedError()

    def _disconnect(self):
        raise NotImplementedError()
