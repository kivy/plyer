'''
Plyer
=====

'''

__all__ = ('accelerometer', 'audio', 'battery', 'browser', 'call', 'camera', 'compass',
           'email', 'filechooser', 'gps', 'gyroscope', 'irblaster',
           'orientation', 'notification', 'sms', 'tts', 'uniqueid', 'vibrator')

__version__ = '1.2.5dev'


from plyer import facades
from plyer.utils import Proxy

#: Accelerometer proxy to :class:`plyer.facades.Accelerometer`
accelerometer = Proxy('accelerometer', facades.Accelerometer)

#: Audio proxy to :class:`plyer.facades.Audio`
audio = Proxy('audio', facades.Audio)

#: Battery proxy to :class:`plyer.facades.Battery`
battery = Proxy('battery', facades.Battery)

#: Browser proxy to :class:`plyer.facades.Browser`
browser = Proxy('browser', facades.Browser)

#: Call proxy to  :class `plyer.facades.Call`
call = Proxy('call', facades.Call)

#: Compass proxy to :class:`plyer.facades.Compass`
compass = Proxy('compass', facades.Compass)

#: Camera proxy to :class:`plyer.facades.Camera`
camera = Proxy('camera', facades.Camera)

#: Email proxy to :class:`plyer.facades.Email`
email = Proxy('email', facades.Email)

#: FileChooser proxy to :class:`plyer.facades.FileChooser`
filechooser = Proxy('filechooser', facades.FileChooser)

#: GPS proxy to :class:`plyer.facades.GPS`
gps = Proxy('gps', facades.GPS)

#: Gyroscope proxy to :class:`plyer.facades.Gyroscope`
gyroscope = Proxy('gyroscope', facades.Gyroscope)

#: IrBlaster proxy to :class:`plyer.facades.IrBlaster`
irblaster = Proxy('irblaster', facades.IrBlaster)

#: Orientation proxy to :class:`plyer.facades.Orientation`
orientation = Proxy('orientation', facades.Orientation)

#: Notification proxy to :class:`plyer.facades.Notification`
notification = Proxy('notification', facades.Notification)

#: Sms proxy to :class:`plyer.facades.Sms`
sms = Proxy('sms', facades.Sms)

#: TTS proxy to :class:`plyer.facades.TTS`
tts = Proxy('tts', facades.TTS)

#: UniqueID proxy to :class:`plyer.facades.UniqueID`
uniqueid = Proxy('uniqueid', facades.UniqueID)

#: Vibrator proxy to :class:`plyer.facades.Vibrator`
vibrator = Proxy('vibrator', facades.Vibrator)

#: Flash proxy to :class:`plyer.facades.Flash`
flash = Proxy('flash', facades.Flash)
