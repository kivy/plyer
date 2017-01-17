'''
Facades
=======

Interface of all the features available.

'''

__all__ = ('Accelerometer', 'Audio', 'Battery', 'Call', 'Camera', 'Compass',
           'Email', 'FileChooser', 'GPS', 'Gyroscope', 'IrBlaster',
           'Orientation', 'Notification', 'QrBarcodeReader', 'Sms',
           'TTS', 'UniqueID', 'Vibrator', 'Wifi', 'Flash')

from plyer.facades.accelerometer import Accelerometer
from plyer.facades.audio import Audio
from plyer.facades.battery import Battery
from plyer.facades.call import Call
from plyer.facades.camera import Camera
from plyer.facades.compass import Compass
from plyer.facades.email import Email
from plyer.facades.filechooser import FileChooser
from plyer.facades.gps import GPS
from plyer.facades.gyroscope import Gyroscope
from plyer.facades.irblaster import IrBlaster
from plyer.facades.orientation import Orientation
from plyer.facades.notification import Notification
from plyer.facades.qrbarcodereader import QrBarcodeReader
from plyer.facades.sms import Sms
from plyer.facades.tts import TTS
from plyer.facades.uniqueid import UniqueID
from plyer.facades.vibrator import Vibrator
from plyer.facades.flash import Flash
from plyer.facades.wifi import Wifi
