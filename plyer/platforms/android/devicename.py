'''
Module of Android API for plyer.devicename.
'''

from jnius import autoclass
from plyer.platforms.android import activity
from plyer.facades import UniqueID

Secure = autoclass('android.provider.Global$Secure')


class AndroidDeviceName(UniqueID):
    '''
    Implementation of Android devicename API.
    '''

    def _get_uid(self):
        return Secure.getString(
            activity.getContentResolver(),
            Secure.DEVICE_NAME
        )


def instance():
    '''
    Instance for facade proxy.
    '''
    return AndroidDeviceName()
