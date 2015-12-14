class Call(object):
    ''' Call facade.
    .. note::
        On Android your app needs the CALL_PHONE permission in order to
        make calls.
    '''

    def makecall(self, tel):
        self._makecall(tel=tel)

    def dialcall(self):
        self._dialcall()

    # private

    def _makecall(self, **kwargs):
        raise NotImplementedError()

    def _dialcall(self, **kwargs):
        raise NotImplementedError()
