from jnius import autoclass, cast
from plyer.platforms.android import activity
from plyer.facades import Battery

Intent = autoclass('android.content.Intent')
BatteryManager = autoclass('android.os.BatteryManager')

class AndroidBattery(Battery):
    def _get_status(self):
        status = {"connected": None, "percentage": None}

        ifilter = cast('android.content.IntentFilter', 
            Intent.ACTION_BATTERY_CHANGED)

        batteryStatus = cast('android.content.Intent', 
            activity.registerReceiver(null, ifilter))

        status = batteryStatus.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
        isCharging = status == BatteryManager.BATTERY_STATUS_CHARGING ||
                     status == BatteryManager.BATTERY_STATUS_FULL;

        level = batteryStatus.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
        scale = batteryStatus.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
        percentage = level / (float)scale

        status['connected'] = isCharging
        status['percentage'] = percentage

        return status
        
def instance():
    return AndroidBattery()