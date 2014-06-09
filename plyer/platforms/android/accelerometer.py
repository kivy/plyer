'''
Android accelerometer
---------------------
'''

from plyer.facades import Accelerometer
from jnius import PythonJavaClass, java_method, autoclass, cast
from plyer.platforms.android import activity

Context = autoclass('android.content.Context')
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')

class AccelerometerSensorListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self):
        super(AccelerometerSensorListener, self).__init__()
        self.SensorManager = cast('android.hardware.SensorManager', 
                    activity.getSystemService(Context.SENSOR_SERVICE))
        self.sensor = self.SensorManager.getDefaultSensor(
                Sensor.TYPE_ACCELEROMETER)
        
        self.ac_x = 0
        self.ac_y = 0
        self.ac_z = 0

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
        self.ac_x = event.values[0]
        self.ac_y = event.values[1]
        self.ac_z = event.values[2]

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor, accuracy):
        # Maybe, do something in future? 
        pass 

class AndroidAccelerometer(Accelerometer):
    def __init__(self):
        super(AndroidAccelerometer, self).__init__()
        self.listener = AccelerometerSensorListener()

    def _enable(self):
        self.listener.enable()

    def _disable(self):
        self.listener.disable()

    def _get_acceleration(self):
        return (self.listener.ac_x, self.listener.ac_y, self.listener.ac_z) 
        
def instance():
    return AndroidAccelerometer()
