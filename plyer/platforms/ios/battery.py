from pyobjus import autoclass
from pyobjus.dylib_manager import load_framework
from plyer.facades import Battery

load_framework('/System/Library/Frameworks/UIKit.framework')
UIDevice = autoclass('UIDevice')


class iOSBattery(Battery):
    def _get_status(self):
        status = {"isCharging": None, "percentage": None}

        currentdevice = UIDevice.currentDevice()
        currentdevice.setBatteryMonitoringEnabled_(True)

        if(currentdevice.batteryMonitoringEnabled):
            if currentdevice.batteryState == 0:
                isCharging = None
            elif currentdevice.batteryState == 2:
                isCharging = True
            else:
                isCharging = False

            percentage = currentdevice.batteryLevel * 100.

            status['isCharging'] = isCharging
            status['percentage'] = percentage

        return status


def instance():
    return iOSBattery()
