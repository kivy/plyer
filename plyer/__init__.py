'''
Plyer
=====

'''

__all__ = ('accelerometer', 'camera', 'gps', 'notification', 'tts', 'email', 'vibrator')
__version__ = '1.1.2'

from plyer import facades
from plyer.utils import Proxy

#: Accelerometer proxy to :class:`plyer.facades.Accelerometer`
accelerometer = Proxy(
    'accelerometer', facades.Accelerometer)

#: Camera proxy to :class:`plyer.facades.Camera`
camera = Proxy(
    'camera', facades.Camera)

#: GPS proxy to :class:`plyer.facades.GPS`
gps = Proxy(
    'gps', facades.GPS)

#: Notification proxy to :class:`plyer.facades.Notification`
notification = Proxy(
    'notification', facades.Notification)

#: TTS proxy to :class:`plyer.facades.TTS`
tts = Proxy(
    'tts', facades.TTS)

#: Email proxy to :class:`plyer.facades.Email`
email = Proxy(
    'email', facades.Email)

#: Vibrate proxy to :class:`plyer.facades.Vibrate`
vibrator = Proxy(
    'vibrator', facades.Vibrator)
