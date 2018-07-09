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
        status = {"isCharging": None, "percentage": None}

        query = battery_status()

        if not query:
            return status

        status["isCharging"] = query["BatteryFlag"] == 8
        status["percentage"] = query["BatteryLifePercent"]

        return status


def instance():
    '''
    Instance for facade proxy.
    '''
    return WinBattery()
