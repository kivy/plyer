from jnius import autoclass
from jnius import cast
from jnius import java_method
from jnius import PythonJavaClass
from plyer.platforms.android import activity
from plyer.facades import GyroUncalibrated

ActivityInfo = autoclass('android.content.pm.ActivityInfo')
Context = autoclass('android.content.Context')
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')


class GyroUncalibratedSensorListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self):
        super(GyroUncalibratedSensorListener, self).__init__()
        service = activity.getSystemService(Context.SENSOR_SERVICE)
        self.SensorManager = cast('android.hardware.SensorManager', service)

        self.sensor = self.SensorManager.getDefaultSensor(
            Sensor.TYPE_GYROSCOPE_UNCALIBRATED)
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


class AndroidGyroUncalibrated(GyroUncalibrated):

    listener = None

    def _get_rotation(self):
        if self.listener and self.listener.values:
            values = self.listener.values
            x_speed, y_speed, z_speed,\
                x_drift, y_drift, z_drift = values[:6]
            return x_speed, y_speed, z_speed, x_drift, y_drift, z_drift

    def _enable_listener(self, **kwargs):
        if not self.listener:
            self.listener = GyroUncalibratedSensorListener()
            self.listener.enable()

    def _disable_listener(self, **kwargs):
        if self.listener:
            self.listener.disable()
            delattr(self, 'listener')


def instance():
    return AndroidGyroUncalibrated()
