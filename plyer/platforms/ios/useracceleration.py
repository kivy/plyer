'''
iOS User Acceleration
---------------------
'''

from plyer.facades import UserAcceleration
from pyobjus import autoclass


class iOSUserAcceleration(UserAcceleration):

    def __init__(self):
        super(iOSUserAcceleration, self).__init__()
        self.bridge = autoclass('bridge').alloc().init()
        self.bridge.motionManager.setDeviceMotionUpdateInterval_(0.1)

    def _enable(self):
        self.bridge.startDeviceMotion()

    def _disable(self):
        self.bridge.stopDeviceMotion()

    def _get_acceleration(self):
        return (
            self.bridge.user_acc_x,
            self.bridge.user_acc_y,
            self.bridge.user_acc_z)


def instance():
    return iOSUserAcceleration()
