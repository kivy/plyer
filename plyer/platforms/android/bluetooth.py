from jnius import autoclass
from plyer.platforms.android import activity
from plyer.facades import Bluetooth

Global = autoclass('android.provider.Settings$Global')


class AndroidBluetooth(Bluetooth):

    def _get_info(self):
        bluetooth_enabled = Global.getString(activity.getContentResolver(), Global.BLUETOOTH_ON)
        if bluetooth_enabled:
            return 'on'
        return 'off'


def instance():
    return AndroidBluetooth()
