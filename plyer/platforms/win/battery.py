from plyer.platforms.win.libs.batterystatus import battery_status
from plyer.facades import Battery

class WinBattery(Battery):
    def _get_status(self):
        status = {"connected": None, "percentage": None}

        query = battery_status()

        if (not query):
            return status

        status["connected"] = query["ACLineStatus"] == 1
        status["percentage"] = query["BatteryLifePercent"]

        return status
        
def instance():
    return WinBattery()