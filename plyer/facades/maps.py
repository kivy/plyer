class Maps(object):

    def locate(self, lc):
        self._locate(lc=lc)

    def _locate(self, **kwargs):
        raise NotImplementedError()
