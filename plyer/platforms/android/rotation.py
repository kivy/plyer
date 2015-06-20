from plyer.facades import Rotation
from jnius import PythonJavaClass, java_method, autoclass, cast
from plyer.platforms.android import activity
from math import pi

Context = autoclass('android.content.Context')
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')


class RotationSensorListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self):
        super(RotationSensorListener, self).__init__()
        self.SensorManager = cast('android.hardware.SensorManager',
                                  activity.getSystemService(Context.SENSOR_SERVICE))
        self.sensor = self.SensorManager.getDefaultSensor(
            Sensor.TYPE_ROTATION_VECTOR)

        # self.value = None
        self.values = [None, None, None]
        self.orientation = [0., 0., 0.]
        self.rMat = [0.] * 9

    def enable(self):
        self.SensorManager.registerListener(self, self.sensor,
                                            SensorManager.SENSOR_DELAY_NORMAL)

    def disable(self):
        self.SensorManager.unregisterListener(self, self.sensor)

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event):
        SensorManager.getRotationMatrixFromVector(self.rMat, event.values[:3])
        # values_ = [azimuth, pitch, roll]
        values_ = SensorManager.getOrientation(self.rMat, self.orientation)[:3]
        values_[0] = (values_[0] * 180 / pi + 360) % 360
        values_[1] = values_[1] * 180 / pi
        values_[2] = values_[2] * 180 / pi
        self.values = values_

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor, accuracy):
        # Maybe, do something in future?
        pass


class AndroidRotation(Rotation):
    def __init__(self):
        super(AndroidRotation, self).__init__()
        self.bState = False

    def _enable(self):
        if not self.bState:
            self.listener = RotationSensorListener()
            self.listener.enable()
            self.bState = True

    def _disable(self):
        if self.bState:
            self.bState = False
            self.listener.disable()
            del self.listener

    def _get_rotation(self):
        if self.bState:
            return tuple(self.listener.values)
        else:
            return None, None, None

    def __del__(self):
        if self.bState:
            self._disable()
        super(self.__class__, self).__del__()


def instance():
    return AndroidRotation()