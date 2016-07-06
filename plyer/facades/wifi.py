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
