class Toast(object):
    '''
     Toast facade.
    '''

    def maketoast(self, text, duration):
        self._maketoast(text=text, duration=duration)

    # private

    def _maketoast(self, **kwargs):
        raise NotImplementedError()
