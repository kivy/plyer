'''
Plyer
=====

'''

__all__ = ('accelerometer', 'camera', 'gps', 'notification',
            'tts', 'email', 'vibrator', 'sms', 'compass',
            'gyroscope', 'uniqueid', 'battery')

__version__ = '1.2.4-dev'

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

#: Vibrate proxy to :class:`plyer.facades.Vibrator`
vibrator = Proxy(
    'vibrator', facades.Vibrator)

#: Sms proxy to :class:`plyer.facades.Sms`
sms = Proxy(
    'sms', facades.Sms)

#: Compass proxy to :class:`plyer.facades.Compass`
compass = Proxy(
    'compass', facades.Compass)

#: Gyroscope proxy to :class:`plyer.facades.Gyroscope`
gyroscope = Proxy(
    'gyroscope', facades.Gyroscope)

#: UniqueID proxy to :class:`plyer.facades.UniqueID`
uniqueid = Proxy(
    'uniqueid', facades.UniqueID)

#: Battery proxy to :class:`plyer.facades.Battery`
battery = Proxy(
    'battery', facades.Battery)
