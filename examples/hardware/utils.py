from jnius import autoclass
from plyer.platforms.android import activity

Context = autoclass('android.content.Context')

AndroidString = autoclass('java.lang.String')
List = autoclass('java.util.List')
ArrayList = autoclass('java.util.ArrayList')


Sensor = autoclass('android.hardware.Sensor')
SensorEvent = autoclass('android.hardware.SensorEvent')
SensorEventListener = autoclass('android.hardware.SensorEventListener')
SensorManager = autoclass('android.hardware.SensorManager')

DisplayMetrics = autoclass('android.util.DisplayMetrics')

PythonActivity = autoclass('org.renpy.android.PythonActivity')
InputMethodManager = autoclass('android.view.inputmethod.InputMethodManager')

ScanResult = autoclass('android.net.wifi.ScanResult')
WifiManager = autoclass('android.net.wifi.WifiManager')
BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
ConnectivityManager = autoclass('android.net.ConnectivityManager')
NetworkInfo = autoclass('android.net.NetworkInfo')

Intent = autoclass('android.content.Intent')
IntentFilter = autoclass('android.content.IntentFilter')


class Utils(object):
    """Class with custom utilities.

    Provides access to display DPI, hardware sensors,
    show and hide keyboard.
    """

    @staticmethod
    def display_metrics():
        """Return display density DPI.

        :return: int display density
        """
        return activity.getResources().getDisplayMetrics().densityDpi

    @staticmethod
    def get_hardware_sensors():
        """Return list about information about hardware sensors.

        Items of list is a dict with keys:
            name str
            vendor str
            version int
            maximum_range float
            min_delay int
            power float
            type int
        """
        sensor_manager = activity.getSystemService(Context.SENSOR_SERVICE)
        sensors = sensor_manager.getSensorList(Sensor.TYPE_ALL)

        result = []
        for sensor in sensors.toArray():
            sensor_data = {
                'name': sensor.getName(),
                'vendor': sensor.getVendor(),
                'version': sensor.getVersion(),
                'maximum_range': sensor.getMaximumRange(),
                'min_delay': sensor.getMinDelay(),
                'power': sensor.getPower(),
                'type': sensor.getType(),
            }
            result.append(sensor_data)
        return result

    @staticmethod
    def show_keyboard():
        """Show keyboard."""
        input_manager = activity.getSystemService(Context.INPUT_METHOD_SERVICE)
        view = PythonActivity.mView
        input_manager.showSoftInput(view, InputMethodManager.SHOW_FORCED)

    @staticmethod
    def hide_keyboard():
        """Hide keyboard."""
        input_manager = activity.getSystemService(Context.INPUT_METHOD_SERVICE)
        view = PythonActivity.mView
        input_manager.hideSoftInputFromWindow(view.getWindowToken(), 0)

    @staticmethod
    def is_connection():
        """Assert is there a connection to internet or not.

        :return: True if connected, False otherwise
        """
        service = Context.CONNECTIVITY_SERVICE
        connection_manager = activity.getSystemService(service)
        active_network = connection_manager.getActiveNetworkInfo()
        return active_network is not None and active_network.isConnected()


def instance():
    return Utils
