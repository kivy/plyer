'''
Module of Windows API for plyer.battery.
'''

from plyer.platforms.win.libs.batterystatus import battery_status
from plyer.facades import Battery


class WinBattery(Battery):
    '''
    Implementation of Windows battery API.
    '''

    def _get_state(self):
        # Flags values
        CHARGING = 8
        NO_SYSTEM_BATTERY = 128
        UNKNOWN_STATUS = 255
        
        status = {"isCharging": None, "percentage": None}

        query = battery_status()

        if not query:
            return status

        status["isCharging"] = (query["BatteryFlag"] != UNKNOWN_STATUS) and \
                               (query["BatteryFlag"] & NO_SYSTEM_BATTERY > 0) and \
                               (query["BatteryFlag"] & CHARGING > 0)
        status["percentage"] = query["BatteryLifePercent"]

        return status


def instance():
    '''
    Instance for facade proxy.
    '''
    return WinBattery()
