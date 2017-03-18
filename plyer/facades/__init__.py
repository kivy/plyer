'''
Facades
=======

Interface of all the features available.

'''

__all__ = ('Accelerometer', 'Audio', 'Barometer', 'Battery', 'Call', 'Camera',
           'Compass', 'Email', 'FileChooser', 'GPS', 'Gravity', 'Gyroscope',
           'IrBlaster', 'Light', 'Orientation', 'Notification', 'Proximity',
           'Sms', 'TTS', 'UniqueID', 'Vibrator', 'Wifi', 'Flash',
           'Temperature')

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
from plyer.facades.tts import TTS
from plyer.facades.uniqueid import UniqueID
from plyer.facades.vibrator import Vibrator
from plyer.facades.wifi import Wifi
from plyer.facades.temperature import Temperature
