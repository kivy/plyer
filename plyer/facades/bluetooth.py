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

    def connect(self, name):
        '''connect to a bluetooth device
        '''
        self._connect(name=name)

    def disconnect(self, name):
        '''disconnect to a bluetooth device
        '''
        self._disconnect(name=name)

    def pair(self, name):
        ''' pair a bluetooth device
        '''
        self._pair(name=name)

    def scan(self):
        ''' Start scanning for nearby bluetooth devices.
        '''
        self._scan()

    def get_paired_devices(self):
        ''' Get list of paired devices.
        '''
        return self._get_paired_devices()

    def get_scan_devices(self):
        ''' Get the scanned devices.
        '''
        return self._get_scan_devices()

    # private

    def _enable(self):
        raise NotImplementedError()

    def _is_enabled(self):
        raise NotImplementedError()

    def _disable(self):
        raise NotImplementedError()

    def _visible(self):
        raise NotImplementedError()

    def _connect(self, **kwargs):
        raise NotImplementedError()

    def _disconnect(self, **kwargs):
        raise NotImplementedError()

    def _pair(self, **kwargs):
        raise NotImplementedError()

    def _scan(self):
        raise NotImplementedError()

    def _get_paired_devices(self):
        raise NotImplementedError()

    def _get_scan_devices(self):
        raise NotImplementedError()
