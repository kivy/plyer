def Fingerprint(object):
    '''
    facade for fingerprint authentication
    '''

    def authenticate(self):
        '''
        start fingerprint authentication
        '''
        self._authenticate()

    def _authenticate(self):
        raise NotImplementedError()
