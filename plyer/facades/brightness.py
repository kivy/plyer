class Brightness(object):
    ''' Brightness facade.
    .. note::
        On Android your app needs the WRITE_SETTINGS permission in order to
        make calls.
    '''

    def set_brightness(self, value=50, time=200):
        self._set_brightness(value=value, time=time)

    def get_brightness(self):
        self._get_brightness()

    def inc_brightness(self, increase_by=10, time=200):
        self._inc_brightness(increase_by=increase_by)

    def dec_brightness(self, decrease_by=10, time=200):
        self._dec_brightness(decrease_by=decrease_by, time=time)

    # private

    def _set_brightness(self, **kwargs):
        raise NotImplementedError()

    def _get_brightness(self, **kwargs):
        raise NotImplementedError()

    def _inc_brightness(self, **kwargs):
        raise NotImplementedError()

    def _dec_brightness(self, **kwargs):
        raise NotImplementedError()
