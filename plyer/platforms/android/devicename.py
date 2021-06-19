'''
Module of Android API for plyer.devicename.
'''

from jnius import autoclass
from plyer.platforms.android import activity
from plyer.facades import DeviceName

Secure = autoclass('android.provider.Global$Secure')


class AndroidDeviceName(DeviceName):
    '''
    Implementation of Android devicename API.
    '''

    def _get_device_name(self):
        return Secure.getString(
            activity.getContentResolver(),
            Secure.DEVICE_NAME
        )


def instance():
    '''
    Instance for facade proxy.
    '''
    return AndroidDeviceName()
