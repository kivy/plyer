from jnius import autoclass
from jnius import cast
from jnius import java_method
from jnius import PythonJavaClass
from plyer.platforms.android import activity
from plyer.facades import MFU

ActivityInfo = autoclass('android.content.pm.ActivityInfo')
Context = autoclass('android.content.Context')
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')


class MFUSensorListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self):
        super(MFUSensorListener, self).__init__()
        service = activity.getSystemService(Context.SENSOR_SERVICE)
        self.SensorManager = cast('android.hardware.SensorManager', service)

        self.sensor = self.SensorManager.getDefaultSensor(
            Sensor.TYPE_MAGNETIC_FIELD_UNCALIBRATED)
        self.values = None

    def enable(self):
        self.SensorManager.registerListener(self, self.sensor,
                    SensorManager.SENSOR_DELAY_NORMAL)

    def disable(self):
        self.SensorManager.unregisterListener(self, self.sensor)

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event):
        self.values = event.values[:6]

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor, accuracy):
        pass


class AndroidMFU(MFU):

    listener = None

    def _get_field(self):
        if self.listener and self.listener.values:
            values = self.listener.values
            x_uncalib, y_uncalib, z_uncalib,\
                x_bias, y_bias, z_bias = values[:6]
            return x_uncalib, y_uncalib, z_uncalib, x_bias, y_bias, z_bias

    def _enable_listener(self, **kwargs):
        if not self.listener:
            self.listener = MFUSensorListener()
            self.listener.enable()

    def _disable_listener(self, **kwargs):
        if self.listener:
            self.listener.disable()
            delattr(self, 'listener')


def instance():
    return AndroidMFU()
