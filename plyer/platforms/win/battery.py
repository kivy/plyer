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
        CHARGING = 8
        UNKNOWN_STATUS = -1
        status = {"isCharging": None, "percentage": None}

        query = battery_status()

        if not query:
            return status

        status["isCharging"] = (query["BatteryFlag"] != UNKNOWN_STATUS) and \
                               (query["BatteryFlag"] & CHARGING > 0)
        status["percentage"] = query["BatteryLifePercent"]

        return status


def instance():
    '''
    Instance for facade proxy.
    '''
    return WinBattery()
