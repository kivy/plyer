from jnius import autoclass
from jnius import cast
from jnius import java_method
from jnius import PythonJavaClass
from plyer.platforms.android import activity
from plyer.facades import SpatialOrientation

ActivityInfo = autoclass('android.content.pm.ActivityInfo')
Context = autoclass('android.content.Context')
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')


class OrientationSensorListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self):
        super(OrientationSensorListener, self).__init__()
        service = activity.getSystemService(Context.SENSOR_SERVICE)
        self.SensorManager = cast('android.hardware.SensorManager', service)

        self.sensor = self.SensorManager.getDefaultSensor(
            Sensor.TYPE_ORIENTATION)
        self.values = None

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


class AndroidOrientation(SpatialOrientation):

    listener = None

    def _set_landscape(self, **kwargs):
        reverse = kwargs.get('reverse')
        if reverse:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_REVERSE_LANDSCAPE)
        else:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE)

    def _set_portrait(self, **kwargs):
        reverse = kwargs.get('reverse')
        if reverse:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_REVERSE_PORTRAIT)
        else:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_PORTRAIT)

    def _set_sensor(self, **kwargs):
        mode = kwargs.get('mode')

        if mode == 'any':
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_SENSOR)
        elif mode == 'landscape':
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE)
        elif mode == 'portrait':
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT)

    def _get_orientation(self):
        if self.listener and self.listener.values:
            values = self.listener.values
            yaw, pitch, roll = values[:3]
            return pitch, roll, yaw

    def _enable_listener(self, **kwargs):
        if not self.listener:
            self.listener = OrientationSensorListener()
            self.listener.enable()

    def _disable_listener(self, **kwargs):
        if self.listener:
            self.listener.disable()
            delattr(self, 'listener')


def instance():
    return AndroidOrientation()
