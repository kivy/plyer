class Wifi(object):
    '''Facade for manipulate wifi.
    '''

    def _enable(self):
        raise NotImplementedError

    def _is_enabled(self):
        raise NotImplementedError

    def _disable(self):
        raise NotImplementedError

    def _start_scanning(self):
        raise NotImplementedError

    def _stop_scanning(self):
        raise NotImplementedError

    def _get_access_points(self):
        raise NotImplementedError

    def enable(self):
        '''Turn on wifi.

        In order to get available access points use after that
        method `get_access_points`.

        .. note::
            Needed Android Permission; ACCESS_NETWORK_STATE
        '''
        self._enable()

    def is_enabled(self):
        '''Return `True` when Wifi is enabled. In other case `False`.

        .. note::
            Needed Android Permission: ACCESS_WIFI_STATE
        :return: True if enabled. Otherwise False.
        '''
        return self._is_enabled()

    def disable(self):
        '''Turn off wifi.'''
        self._disable()

    def start_scanning(self):
        '''Turn on scanning.'''
        self._start_scanning()

    def stop_scanning(self):
        '''Turn off scanning.

        .. note::
            Android doesn't provides any methods for stop scanning.
            One trick is to connect to device.
        '''
        self._stop_scanning()

    def get_access_points(self):
        '''Return list of available to connect access points.'''
        return self._get_access_points()
