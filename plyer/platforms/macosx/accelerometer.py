'''
MacOSX accelerometer
---------------------
'''

from plyer.facades import Accelerometer
from plyer.platforms.macosx import motionsensor

class OSXAccelerometer(Accelerometer):

    def _enable(self):
        return motionsensor.is_available()

    def _disable(self):
        pass

    def _get_acceleration(self):
        return motionsensor.get_coord()
        
def instance():
    return OSXAccelerometer()
