'''
Module of Android API for plyer.battery.
'''

from jnius import autoclass, cast  # pylint: disable=no-name-in-module
from plyer.platforms.android import activity
from plyer.facades import Battery

INTENT = autoclass('android.content.Intent')
BATTERYMANAGER = autoclass('android.os.BatteryManager')
INTENTFILTER = autoclass('android.content.IntentFilter')


class AndroidBattery(Battery):
    '''
    Implementation of Android battery API.
    '''

    def _get_state(self):
        status = {"isCharging": None, "percentage": None}

        ifilter = INTENTFILTER(INTENT.ACTION_BATTERY_CHANGED)

        battery_status = cast(
            'android.content.INTENT',
            activity.registerReceiver(None, ifilter)
        )

        query = battery_status.getIntExtra(BATTERYMANAGER.EXTRA_STATUS, -1)
        is_charging = query == BATTERYMANAGER.BATTERY_STATUS_CHARGING
        is_full = query == BATTERYMANAGER.BATTERY_STATUS_FULL

        level = battery_status.getIntExtra(BATTERYMANAGER.EXTRA_LEVEL, -1)
        scale = battery_status.getIntExtra(BATTERYMANAGER.EXTRA_SCALE, -1)
        percentage = (level / float(scale)) * 100

        status['isCharging'] = is_charging or is_full
        status['percentage'] = percentage

        return status


def instance():
    '''
    Instance for facade proxy.
    '''
    return AndroidBattery()
