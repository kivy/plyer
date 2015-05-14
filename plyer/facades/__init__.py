'''
Facades
=======

Interface of all the features available.

'''

__all__ = ('Accelerometer', 'Battery', 'Camera', 'Compass', 'Email',
           'FileChooser', 'GPS', 'Gyroscope', 'IrBlaster', 'Orientation',
           'Notification', 'Sms', 'Speech', 'TTS', 'UniqueID', 'Vibrator')

from plyer.facades.accelerometer import Accelerometer
from plyer.facades.battery import Battery
from plyer.facades.camera import Camera
from plyer.facades.compass import Compass
from plyer.facades.email import Email
from plyer.facades.filechooser import FileChooser
from plyer.facades.gps import GPS
from plyer.facades.gyroscope import Gyroscope
from plyer.facades.irblaster import IrBlaster
from plyer.facades.orientation import Orientation
from plyer.facades.notification import Notification
from plyer.facades.sms import Sms
from plyer.facades.speech import Speech
from plyer.facades.tts import TTS
from plyer.facades.uniqueid import UniqueID
from plyer.facades.vibrator import Vibrator
