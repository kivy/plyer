'''
Facades
=======

Interface of all the features available.

'''

__all__ = ('Accelerometer', 'Audio', 'Barometer', 'Battery', 'Bluetooth',
           'Brightness', 'Call', 'Camera','CPU', 'Compass', 'DeviceName',
           'Email', 'FileChooser', 'Flash', 'GPS','Gravity', 'Gyroscope',
           'IrBlaster', 'Keystore', 'Light', 'Maps', 'Notification',
           'Orientation', 'Proximity', 'Sms', 'Sysinfo', 'SpatialOrientation',
           'Screenshot', 'StoragePath','STT', 'TTS', 'UniqueID', 'Vibrator',
           'Wifi', 'Temperature', 'Humidity', 'Processors', )

from plyer.facades.accelerometer import Accelerometer
from plyer.facades.audio import Audio
from plyer.facades.barometer import Barometer
from plyer.facades.battery import Battery
from plyer.facades.call import Call
from plyer.facades.camera import Camera
from plyer.facades.compass import Compass
from plyer.facades.email import Email
from plyer.facades.filechooser import FileChooser
from plyer.facades.flash import Flash
from plyer.facades.gps import GPS
from plyer.facades.gravity import Gravity
from plyer.facades.gyroscope import Gyroscope
from plyer.facades.irblaster import IrBlaster
from plyer.facades.light import Light
from plyer.facades.proximity import Proximity
from plyer.facades.orientation import Orientation
from plyer.facades.notification import Notification
from plyer.facades.sms import Sms
from plyer.facades.stt import STT
from plyer.facades.sysinfo import Sysinfo
from plyer.facades.tts import TTS
from plyer.facades.uniqueid import UniqueID
from plyer.facades.vibrator import Vibrator
from plyer.facades.wifi import Wifi
from plyer.facades.temperature import Temperature
from plyer.facades.humidity import Humidity
from plyer.facades.spatialorientation import SpatialOrientation
from plyer.facades.brightness import Brightness
from plyer.facades.keystore import Keystore
from plyer.facades.storagepath import StoragePath
from plyer.facades.bluetooth import Bluetooth
from plyer.facades.processors import Processors
from plyer.facades.cpu import CPU
from plyer.facades.screenshot import Screenshot
from plyer.facades.devicename import DeviceName
from plyer.facades.maps import Maps
