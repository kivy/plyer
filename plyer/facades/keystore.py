class Keystore(object):
    '''
    Keyring facade

    .. versionadded:: x.x.x

    '''

    def set_key(self, servicename, key, value, **kwargs):
        self._set_password(servicename, key, value, **kwargs)

    def _set_key(self, servicename, key, value, **kwargs):
        raise NotImplementedError()

    def get_key(self, servicename, key, **kwargs):
        return self._get_password(servicename, username)

    def _get_key(self, servicename, key, **kwargs):
        raise NotImplementedError()