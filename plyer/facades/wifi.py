class Wifi(object):
    '''Wifi Facade.
    '''

    def enable(self):
        '''
        Turn on wifi.
        '''
        self._enable()

    def is_enabled(self):
        '''
        Returns `True`if the Wifi is enables else `False`.
        '''
        return self._is_enabled()

    def disable(self):
        '''
        Turn off wifi.
        '''
        self._disable()

    def start_scanning(self):
        '''
        Turn on scanning.
        '''
        self._start_scanning()

    def stop_scanning(self):
        '''
        Turn off scanning.
            Note: Access not provided by Apple.
        '''
        self._stop_scanning()

    def get_network_info(self, name):
        '''
        Return a dictionary of secified network.
        '''
        return self._get_access_points(name=name)

    def available_wifi(self):
        '''
        Returns a list of all the available wifi.
        '''

    # private

    def _enable(self):
        raise NotImplementedError()

    def _is_enabled(self):
        raise NotImplementedError()

    def _disable(self):
        raise NotImplementedError()

    def _start_scanning(self):
        raise NotImplementedError()

    def _stop_scanning(self):
        raise NotImplementedError()

    def _get_network_info(self, **kwargs):
        raise NotImplementedError()

    def _available_wifi(self):
        raise NotImplementedError()
