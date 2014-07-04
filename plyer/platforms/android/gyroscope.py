'''
Android Gyroscope
---------------------
'''

from plyer.facades import Gyroscope
from jnius import PythonJavaClass, java_method, autoclass, cast
from plyer.platforms.android import activity

Context = autoclass('android.content.Context')
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')


class GyroscopeSensorListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self):
        super(GyroscopeSensorListener, self).__init__()
        self.SensorManager = cast('android.hardware.SensorManager',
                    activity.getSystemService(Context.SENSOR_SERVICE))
        self.sensor = self.SensorManager.getDefaultSensor(
                Sensor.TYPE_GYROSCOPE)

        self.values = [0, 0, 0]

    def enable(self):
        self.SensorManager.registerListener(self, self.sensor,
                    SensorManager.SENSOR_DELAY_NORMAL)

    def disable(self):
        self.SensorManager.unregisterListener(self, self.sensor)

    @java_method('()I')
    def hashCode(self):
        return id(self)

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event):
        self.values = event.values[:3]

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor, accuracy):
        # Maybe, do something in future?
        pass


class AndroidGyroscope(Gyroscope):
    def __init__(self):
        super(AndroidGyroscope, self).__init__()
        self.listener = GyroscopeSensorListener()

    def _enable(self):
        self.listener.enable()

    def _disable(self):
        self.listener.disable()

    def _get_orientation(self):
        return tuple(self.listener.values)


def instance():
    return AndroidGyroscope()
