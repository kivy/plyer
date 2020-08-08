class Keystore:
    '''
    Keyring facade

    .. versionadded:: x.x.x

    '''

    def set_key(self, servicename, key, value, **kwargs):
        self._set_key(servicename, key, value, **kwargs)

    def _set_key(self, servicename, key, value, **kwargs):
        raise NotImplementedError()

    def get_key(self, servicename, key, **kwargs):
        return self._get_key(servicename, key)

    def _get_key(self, servicename, key, **kwargs):
        raise NotImplementedError()
