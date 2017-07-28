'''
iOS Proximity
-------------
'''

from pyobjus import autoclass
from pyobjus.dylib_manager import load_framework
from plyer.facades import Proximity

load_framework('/System/Library/Frameworks/UIKit.framework')
UIDevice = autoclass('UIDevice')


class iOSProximity(Proximity):

    def __init__(self):
        super(iOSProximity, self).__init__()
        self.device = UIDevice.currentDevice()

    def _enable(self):
        self.device.setProximityMonitoringEnabled_(True)

    def _disable(self):
        self.device.setProximityMonitoringEnabled_(False)

    def _get_proximity(self):
        if self.device.proximityMonitoringEnabled:
            if self.device.proximityState:
                return str(True)
            else:
                return str(False)
        else:
            return 'Proximity Sensor in present in your device.'


def instance():
    return iOSProximity()
