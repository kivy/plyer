try:
    import keyring
except:
    raise NotImplemented()
from plyer.facades import Keystore


class OSXKeystore(Keystore):

    def _set_password(self, servicename, username, password):
        keyring.set_password(servicename, username, password)

    def _get_password(self, servicename, username):
        return keyring.get_password(servicename, username)


def instance():
    return OSXKeystore()
