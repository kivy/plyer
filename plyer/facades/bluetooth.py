class Bluetooth(object):
    '''Bluetooth facade.

    '''

    def start(self):
        '''Start the Bluetooth.
        '''
        self._start()

    def stop(self):
        '''Stop the Bluetooth.
        '''
        self._stop()

    def visible(self):
        '''Turn on Bluetooth visiblity
        '''
        self._visible()

    def on_resume(self):
        '''onResume event handler for the Bluetooth.
        '''
        self._on_resume()

    def on_stop(self):
        '''onStop event handler the Bluetooth.
        '''
        self._on_stop()

    def on_pause(self):
        '''onPause event handler the Bluetooth.
        '''
        self._on_pause()

    # private

    def _start(self):
        raise NotImplementedError()

    def _stop(self):
        raise NotImplementedError()

    def _visible(self):
        raise NotImplementedError()

    def _on_pause(self):
        raise NotImplementedError()

    def _on_resume(self):
        raise NotImplementedError()

    def _on_stop(self):
        raise NotImplementedError()
