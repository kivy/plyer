'''
iOS Gyroscope
---------------------
'''

from plyer.facades import Gyroscope
from pyobjus import autoclass


class IosGyroscope(Gyroscope):

    def __init__(self):
        super(IosGyroscope, self).__init__()
        self.bridge = autoclass('bridge').alloc().init()
        self.bridge.motionManager.setGyroscopeUpdateInterval_(0.1)

    def _enable(self):
        self.bridge.startGyroscope()

    def _disable(self):
        self.bridge.stopGyroscope()

    def _get_orientation(self):
        return (
            self.bridge.gy_x,
            self.bridge.gy_y,
            self.bridge.gy_z)


def instance():
    return IosGyroscope()
