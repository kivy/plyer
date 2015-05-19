class Utils(object):
    '''Facade with custom platform utilities.

    Provides access to:
        * screen metrics (method `display_metrics`).
        * information about hardware sensors (method `get_hardware_sensors`).
        * hiding and showing up keyboard on the screen (methods `show_keyboard`
          and `hide_keyboard`).
        * for start/stop wifi user respectively methods `start_wifi`
          and `stop_wifi`.
        * for get list of Access Points use `get_wifi_scans`.

    .. versionadded:: 1.2.4
    '''

    def start_wifi(self):
        '''Turn on wifi scanner.

        In order to get available access points use after that
        method `get_wifi_scans`.

        .. note::
            Needed Android Permission; ACCESS_NETWORK_STATE
        '''
        self._start_wifi()

    def stop_wifi(self):
        '''Turn off wifi scanner.'''
        self._stop_wifi()

    def get_wifi_scans(self):
        '''Return list of available access points.

        .. note::
            Needed Android Permission: CHANGE_WIFI_STATE
        :return: list of scanned access points. Items of list are a type
                 of dictionary with keys: `ssid`, `bssid`, `level`.
        '''
        return self._get_wifi_scans()

    def is_wifi_enabled(self):
        '''Return `True` when Wifi is enabled. In other case `False`.

        .. note::
            Needed Android Permission: ACCESS_WIFI_STATE
        :return:
        '''
        return self._is_wifi_enabled()

    def display_metrics(self):
        '''Return display density DPI.

        :return: int display density
        '''
        return self._display_metrics()

    def get_hardware_sensors(self):
        '''Return list about information about hardware sensors.

        Items of list is a dictionary type with keys:
            name: type `str`
            vendor: type `str`
            version: type `int`
            maximum_range: type `float`
            min_delay: type `int`
            power: type `float`
            type: type `int`
        '''
        return self._get_hardware_sensors()

    def show_keyboard(self):
        '''Show keyboard on the screen.'''
        self._show_keyboard()

    def hide_keyboard(self):
        '''Hide keyboard on the screen.'''
        self._hide_keyboard()

    def is_connection(self):
        '''Assert is there is a internet connection or not.

        .. note::
            Needed Android Permission: INTERNET

        :return: `True` if connected, `False` otherwise
        '''
        return self._is_connection()

    # Private Methods
    def _start_wifi(self):
        raise NotImplementedError

    def _stop_wifi(self):
        raise NotImplementedError

    def _get_wifi_scans(self):
        raise NotImplementedError

    def _is_wifi_enabled(self):
        raise NotImplementedError

    def _get_hardware_sensors(self):
        raise NotImplementedError

    def _show_keyboard(self):
        raise NotImplementedError

    def _hide_keyboard(self):
        raise NotImplementedError

    def _is_connection(self):
        raise NotImplementedError

    def _display_metrics(self):
        raise NotImplementedError
