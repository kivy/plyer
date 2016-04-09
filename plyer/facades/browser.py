class Browser(object):
    '''Browser facade.
    .. versionadded:: ???

    '''

    def open(self, uri):
        self._open(uri=uri)

    # private

    def _open(self, **kwargs):
        raise NotImplementedError()
