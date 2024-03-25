'''
Plyer
=====

'''

__all__ = (
    'accelerometer', 'audio', 'barometer', 'battery', 'bluetooth',
    'brightness', 'call', 'camera', 'compass', 'cpu', 'devicename', 'email',
    'filechooser', 'flash', 'gps', 'gravity', 'gyroscope', 'humidity', 'irblaster',
    'keystore', 'light', 'maps', 'notification', 'orientation', 'processors',
    'proximity', 'screenshot', 'sms', 'sysinfo', 'spatialorientation',
    'storagepath', 'stt', 'temperature', 'tts', 'uniqueid', 'vibrator', 'wifi'
)

__version__ = '2.2.0.dev0'


from plyer import facades
from plyer.utils import Proxy

#: Accelerometer proxy to :class:`plyer.facades.Accelerometer`
accelerometer = Proxy('accelerometer', facades.Accelerometer)

#: Audio proxy to :class:`plyer.facades.Audio`
audio = Proxy('audio', facades.Audio)

#: Barometer proxy to :class:`plyer.facades.Barometer`
barometer = Proxy('barometer', facades.Barometer)

#: Battery proxy to :class:`plyer.facades.Battery`
battery = Proxy('battery', facades.Battery)

#: Bluetooth proxy to :class:`plyer.facades.Bluetooth`
bluetooth = Proxy('bluetooth', facades.Bluetooth)

#: Brightness proxy to :class:`plyer.facades.Brightness`
brightness = Proxy('brightness', facades.Brightness)

#: Call proxy to  :class `plyer.facades.Call`
call = Proxy('call', facades.Call)

#: Camera proxy to :class:`plyer.facades.Camera`
camera = Proxy('camera', facades.Camera)

#: Compass proxy to :class:`plyer.facades.Compass`
compass = Proxy('compass', facades.Compass)

#: Processors proxy to :class:`plyer.facades.CPU`
cpu = Proxy('cpu', facades.CPU)

#: devicename proxy to :class:`plyer.facades.DeviceName`
devicename = Proxy('devicename', facades.DeviceName)

#: Email proxy to :class:`plyer.facades.Email`
email = Proxy('email', facades.Email)

#: FileChooser proxy to :class:`plyer.facades.FileChooser`
filechooser = Proxy('filechooser', facades.FileChooser)

#: Flash proxy to :class:`plyer.facades.Flash`
flash = Proxy('flash', facades.Flash)

#: GPS proxy to :class:`plyer.facades.GPS`
gps = Proxy('gps', facades.GPS)

#: Gravity proxy to :class:`plyer.facades.Gravity`
gravity = Proxy('gravity', facades.Gravity)

#: Gyroscope proxy to :class:`plyer.facades.Gyroscope`
gyroscope = Proxy('gyroscope', facades.Gyroscope)

#: Humidity proxy to :class:`plyer.facades.Humidity`
humidity = Proxy('humidity', facades.Humidity)

#: IrBlaster proxy to :class:`plyer.facades.IrBlaster`
irblaster = Proxy('irblaster', facades.IrBlaster)

#: Keyring proxy to :class::`plyer.facades.Keystore`
keystore = Proxy('keystore', facades.Keystore)

#: Light proxy to :class:`plyer.facades.Light`
light = Proxy('light', facades.Light)

#: Maps proxy to :class:`plyer.facades.Maps`
maps = Proxy('maps', facades.Maps)

#: Notification proxy to :class:`plyer.facades.Notification`
notification = Proxy('notification', facades.Notification)

#: Orientation proxy to :class:`plyer.facades.Orientation`
orientation = Proxy('orientation', facades.Orientation)

#: Processors proxy to :class:`plyer.facades.Processors`
processors = Proxy('processors', facades.Processors)

#: Proximity proxy to :class:`plyer.facades.Proximity`
proximity = Proxy('proximity', facades.Proximity)

#: Sms proxy to :class:`plyer.facades.Sms`
sms = Proxy('sms', facades.Sms)

#: Screenshot proxy to :class:`plyer.facades.Screenshot`
screenshot = Proxy('screenshot', facades.Screenshot)

#: Sysinfo proxy to :class:`plyer.facades.Screenshot`
sysinfo = Proxy('sysinfo', facades.Sysinfo)

#: SpatialOrientation proxy to :class:`plyer.facades.SpatialOrientation`
spatialorientation = Proxy('spatialorientation', facades.SpatialOrientation)

#: StoragePath proxy to :class:`plyer.facades.StoragePath`
storagepath = Proxy('storagepath', facades.StoragePath)

#: Speech proxy to :class:`plyer.facades.STT`
stt = Proxy('stt', facades.STT)

#: Temperature proxy to :class:`plyer.facades.Temperature`
temperature = Proxy('temperature', facades.Temperature)

#: TTS proxy to :class:`plyer.facades.TTS`
tts = Proxy('tts', facades.TTS)

#: UniqueID proxy to :class:`plyer.facades.UniqueID`
uniqueid = Proxy('uniqueid', facades.UniqueID)

#: Vibrator proxy to :class:`plyer.facades.Vibrator`
vibrator = Proxy('vibrator', facades.Vibrator)

#: Wifi proxy to :class:`plyer.facades.Wifi`
wifi = Proxy('wifi', facades.Wifi)
