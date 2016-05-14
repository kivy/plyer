class Keystore(object):
    '''
    Keyring facade

    .. versionadded:: x.x.x

    '''

    def set_password(self, servicename, username, password):
        self._set_password(servicename, username, password)

    def _set_password(self, servicename, username, password):
        raise NotImplementedError()

    def get_password(self, servicename, username):
        return self._get_password(servicename, username)

    def _get_password(self, servicename, username):
        raise NotImplementedError()