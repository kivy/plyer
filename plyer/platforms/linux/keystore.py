try:
    import keyring
except ImportError:
    raise NotImplementedError()

from plyer.facades import Keystore


class LinuxKeystore(Keystore):

    def _set_key(self, servicename, key, value, *args, **kwargs):
        keyring.set_password(servicename, key, value)

    def _get_key(self, servicename, key, *args, **kwargs):
        return keyring.get_password(servicename, key)


def instance():
    return LinuxKeystore()
