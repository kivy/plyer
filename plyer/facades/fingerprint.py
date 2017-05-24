class Fingerprint(object):
    '''
    Fingerprint facade.
    '''

    def check_hardware(self):
        return self._check_hardware()

    def is_enrolled(self):
        return self._is_enrolled()

    def authenticate(self):
        return self._authenticate()

    #private

    def _check_hardware(self):
        raise NotImplementedError()

    def _is_enrolled(self):
        raise NotImplementedError()

    def _authenticate(self):
        raise NotImplementedError()
