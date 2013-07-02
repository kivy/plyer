'''
Plyer
=====

'''

from plyer import facades
from plyer.utils import Proxy

#: accelerometer proxy
accelerometer = Proxy(
    'accelerometer', facades.Accelerometer)

#: camera proxy
camera = Proxy(
    'camera', facades.Camera)

#: notification proxy
notification = Proxy(
    'notification', facades.Notification)

