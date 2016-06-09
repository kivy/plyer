class NFC(object):
    ''' NFC facade.
    .. note::
        On Android your app needs the NFC permission.
    '''

    def read_tag(self):
        self._read_tag()

    def write_tag(self):
        self._write_tag()

    def nfc_enable_ndef_exchange(self):
        self._nfc_enable_ndef_exchange()

    def nfc_disable_ndef_exchange(self):
        self._nfc_disable_ndef_exchange()

    def on_pause(self):
        self._on_pause()

    def on_resume(self):
        self._on_resume()

    def enable(self):
        self._enable()

    def disable(self):
        self._disable()

    # private

    def _read_tag(self, **kwargs):
        raise NotImplementedError()

    def _write_tag(self, **kwargs):
        raise NotImplementedError()

    def _nfc_enable_ndef_exchange(self, **kwargs):
        raise NotImplementedError()

    def _nfc_disable_ndef_exchange(self, **kwargs):
        raise NotImplementedError()

    def _on_pause(self, **kwargs):
        raise NotImplementedError()
    
    def _on_resume(self, **kwargs):
        raise NotImplementedError()

    def _enable(self, **kwargs):
        raise NotImplementedError()

    def _diable(self, **kwargs):
        raise NotImplementedError()
