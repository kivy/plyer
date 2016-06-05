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

    def on_resume(self):
        '''Called when app is resumed
        '''
        self._on_resume()

    def on_pause(self):
        '''Called when app is paused
        '''
        self._on_pause()

    def register_receiver(self):
        ''' Register Receiver for bluetooth
        '''
        self._register_receiver()

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

    def _on_resume(self):
        raise NotImplementedError()

    def _on_pause(self):
        raise NotImplementedError()

    def _register_receiver(self):
        raise NotImplementedError()

    def _start_discovery(self):
        raise NotImplementedError()

    def _get_paired_devices(self):
        raise NotImplementedError()

    def _get_scan_devices(self):
        raise NotImplementedError()
