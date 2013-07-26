'''
Plyer
=====

'''

__all__ = ('accelerometer', 'camera', 'notification', 'tts')

from plyer import facades
from plyer.utils import Proxy

#: Accelerometer proxy to :class:`plyer.facades.Accelerometer`
accelerometer = Proxy(
    'accelerometer', facades.Accelerometer)

#: Camera proxy to :class:`plyer.facades.Camera`
camera = Proxy(
    'camera', facades.Camera)

#: Notification proxy to :class:`plyer.facades.Notification`
notification = Proxy(
    'notification', facades.Notification)

#: TTS proxy to :class:`plyer.facades.TTS`
tts = Proxy(
    'tts', facades.TTS)
