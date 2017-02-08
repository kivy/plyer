'''
Android gravity
---------------------
'''

from jnius import autoclass
from jnius import cast
from jnius import java_method
from jnius import PythonJavaClass

from plyer.facades import Gravity
from plyer.platforms.android import activity

Context = autoclass('android.content.Context')
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')


class GravitySensorListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self):
        super(GravitySensorListener, self).__init__()

        service = activity.getSystemService(Context.SENSOR_SERVICE)
        self.SensorManager = cast('android.hardware.SensorManager', service)

        self.sensor = self.SensorManager.getDefaultSensor(
            Sensor.TYPE_GRAVITY
        )

        self.values = [None, None, None]

    def enable(self):
        self.SensorManager.registerListener(
            self,
            self.sensor,
            SensorManager.SENSOR_DELAY_NORMAL
        )

    def disable(self):
        self.SensorManager.unregisterListener(self, self.sensor)

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event):
        self.values = event.values[:3]

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor, accuracy):
        pass


class AndroidGravity(Gravity):

    listener = None

    def _enable(self):
        if not self.listener:
            self.listener = GravitySensorListener()
            self.listener.enable()

    def _disable(self):
        if self.listener:
            self.listener.disable()
            del self.listener

    def _get_gravity(self):
        if self.listener:
            return tuple(self.listener.values)
        else:
            return (None, None, None)

    def __del__(self):
        if self.listener:
            self._disable()
        super(self.__class__, self).__del__()


def instance():
return AndroidGravity()