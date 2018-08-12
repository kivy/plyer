'''
Module of Android API for plyer.bluetooth.
'''

from jnius import autoclass
from plyer.platforms.android import activity
from plyer.facades import Bluetooth

GLOBAL = autoclass('android.provider.Settings$Global')


class AndroidBluetooth(Bluetooth):
    '''
    Implementation of Android Bluetooth API.
    '''

    def _get_info(self):
        bluetooth_enabled = GLOBAL.getString(
            activity.getContentResolver(),
            GLOBAL.BLUETOOTH_ON
        )
        status = 'off'
        if bluetooth_enabled:
            status = 'on'
        return status


def instance():
    '''
    Instance for facade proxy.
    '''
    return AndroidBluetooth()
