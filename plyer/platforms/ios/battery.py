from pyobjus import autoclass
from pyobjus.dylib_manager import load_framework
from plyer.facades import Battery

load_framework('/System/Library/Frameworks/UIKit.framework')
UIDevice = autoclass('UIDevice')


class iOSBattery(Battery):
    def __init__(self):
        super(iOSBattery, self).__init__()
        self.device = UIDevice.currentDevice()

    def _get_state(self):
        status = {"isCharging": None, "percentage": None}

        if(not self.device.batteryMonitoringEnabled):
            self.device.setBatteryMonitoringEnabled_(True)

        if self.device.batteryState == 0:
            isCharging = None
        elif self.device.batteryState == 2:
            isCharging = True
        else:
            isCharging = False

        percentage = self.device.batteryLevel * 100.

        status['isCharging'] = isCharging
        status['percentage'] = percentage

        return status


def instance():
    return iOSBattery()
