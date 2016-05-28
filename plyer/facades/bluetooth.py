class Bluetooth(object):
    '''Bluetooth facade.

    '''

    def enable(self):
        '''Start the Bluetooth.
        '''
        self._enable()

    def is_enabled(self):
        ''' Return 'True' if Bluetooth is enabled.
        '''
        self._is_enabled()

    def disable(self):
        '''Stop the Bluetooth.
        '''
        self._disable()

    def visible(self):
        '''Turn on Bluetooth visiblity
        '''
        self._visible()

    def on_stop(self):
        '''onStop event handler the Bluetooth.
        '''
        self._on_stop()

    def start_discovery(self):
        ''' Start scanning for nearby bluetooth devices.
        '''
        self._start_discovery()

    def get_paired_devices(self):
        ''' Get list of paired devices.
        '''
        self._get_paired_devices()

    def get_scan_devices(self):
        ''' Get the scanned devices.
        '''
        self._get_scan_devices()

    # private

    def _enable(self):
        raise NotImplementedError()

    def _is_enabled(self):
        raise NotImplementedError()

    def _disable(self):
        raise NotImplementedError()

    def _visible(self):
        raise NotImplementedError()

    def _on_stop(self):
        raise NotImplementedError()

    def _start_discovery(self):
        raise NotImplementedError()

    def _get_paired_devices(self):
        raise NotImplementedError()

    def _get_scan_devices(self):
        raise NotImplementedError()
