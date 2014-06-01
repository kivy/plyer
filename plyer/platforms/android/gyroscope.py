'''
Android Gyroscope
---------------------
'''

from plyer.facades import Gyroscope
from jnius import autoclass

Hardware = autoclass('org.renpy.android.Hardware')

class AndroidGyroscope(Gyroscope):

    def _enable(self):
        Hardware.orientationSensorEnable(True)

    def _disable(self):
        Hardware.orientationSensorEnable(False)

    def _get_orientation(self):
        return Hardware.orientationSensorReading()

def instance():
    return AndroidGyroscope()
