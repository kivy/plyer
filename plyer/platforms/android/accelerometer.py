'''
Android accelerometer
---------------------
'''

from plyer.facades import Accelerometer
from jnius import autoclass

Hardware = autoclass('org.renpy.android.Hardware')

class AndroidAccelerometer(Accelerometer):

    def enable(self):
        Hardware.accelerometerEnable(True)

    def disable(self):
        Hardware.accelerometerEnable(False)

    def get_acceleration(self):
        return Hardware.accelerometerReading()

def instance():
    return AndroidAccelerometer()
