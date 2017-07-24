'''
Android User Acceleration
-------------------------
'''

from plyer.facades import UserAcceleration
from jnius import PythonJavaClass
from jnius import java_method
from jnius import autoclass
from jnius import cast
from plyer.platforms.android import activity

Context = autoclass('android.content.Context')
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')


class UserAccSensorListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self):
        super(UserAccSensorListener, self).__init__()
        self.SensorManager = cast('android.hardware.SensorManager',
                    activity.getSystemService(Context.SENSOR_SERVICE))
        self.sensor = self.SensorManager.getDefaultSensor(
                Sensor.TYPE_LINEAR_ACCELERATION)

        self.values = [None, None, None]

    def enable(self):
        self.SensorManager.registerListener(self, self.sensor,
                    SensorManager.SENSOR_DELAY_NORMAL)

    def disable(self):
        self.SensorManager.unregisterListener(self, self.sensor)

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event):
        self.values = event.values[:3]

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor, accuracy):
        pass


class AndroidUserAcc(UserAcceleration):

    def __init__(self):
        super(AndroidUserAcc, self).__init__()
        self.state = False

    def _enable(self):
        if not self.state:
            self.listener = UserAccSensorListener()
            self.listener.enable()
            self.state = True

    def _disable(self):
        if self.state:
            self.state = False
            self.listener.disable()
            del self.listener

    def _get_acceleration(self):
        if self.state:
            return tuple(self.listener.values)
        else:
            return (None, None, None)

    def __del__(self):
        if self.state:
            self.disable()
        super(self.__class__, self).__del__()


def instance():
    return AndroidUserAcc()
