from jnius import autoclass
from jnius import cast
from jnius import java_method
from jnius import PythonJavaClass

from plyer.facades import Utils
from plyer.platforms.android import activity

Context = autoclass('android.content.Context')
ConnectivityManager = autoclass('android.net.ConnectivityManager')
DisplayMetrics = autoclass('android.util.DisplayMetrics')
GenericBroadcastReceiver = autoclass(
    'org.renpy.android.GenericBroadcastReceiver'
)
InputMethodManager = autoclass('android.view.inputmethod.InputMethodManager')
Intent = autoclass('android.content.Intent')
IntentFilter = autoclass('android.content.IntentFilter')
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Sensor = autoclass('android.hardware.Sensor')
WifiManager = autoclass('android.net.wifi.WifiManager')


class AndroidUtils(Utils):
    '''Android Utils implementation.

    With `wifi_manager` variable we can start and stop wifi scanning.
    With `wifi_scanner` variable we can listen for available access points.
    Variable `scanned_results` stores list of found access points
    by `wifi_scanner`.
    '''

    wifi_manager = None
    wifi_scanner = None
    scanned_results = None

    class BroadcastReceiver(PythonJavaClass):
        '''Private class for receiving results from wifi manager.'''
        __javainterfaces__ = [
            'org/renpy/android/GenericBroadcastReceiverCallback'
        ]
        __javacontext__ = 'app'

        scan_results = None

        def __init__(self, utils, *args, **kwargs):
            PythonJavaClass.__init__(self, *args, **kwargs)
            self.utils = utils

        @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
        def onReceive(self, context, intent):
            '''Receive list of available access points from wifi and saves
            this list in `scanned_results`.

            :param context: our activity
            '''
            wifi_service = context.getSystemService(Context.WIFI_SERVICE)
            wifi_manager = cast('android.net.wifi.WifiManager', wifi_service)
            self.utils.scanned_results = wifi_manager.getScanResults()

    def __init__(self):
        super(AndroidUtils, self).__init__()
        wifi_service = activity.getSystemService(Context.WIFI_SERVICE)
        self.wifi_manager = cast('android.net.wifi.WifiManager', wifi_service)

    def _start_wifi(self):
        broadcast_receiver = AndroidUtils.BroadcastReceiver(self)
        self.wifi_scanner = GenericBroadcastReceiver(broadcast_receiver)
        intent_filter = IntentFilter()
        intent_filter.addAction(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION)
        activity.registerReceiver(self.wifi_scanner, intent_filter)

    def _stop_wifi(self):
        activity.unregisterReceiver(self.wifi_scanner)

    def _get_wifi_scans(self):
        if not self.scanned_results:
            self.wifi_manager.startScan()
            return None

        access_points = []
        scanned_points = self.scanned_results.toArray()
        for access in scanned_points:
            access_point = {
                'ssid': access.SSID,
                'bssid': access.BSSID,
                'level': access.level
            }
            access_points.append(access_point)

        self.wifi_manager.startScan()
        return access_points

    def _is_wifi_enabled(self):
        return self.wifi_manager and self.wifi_manager.isWifiEnabled()

    def _display_metrics(self):
        return activity.getResources().getDisplayMetrics().densityDpi

    def _get_hardware_sensors(self):
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

    def _show_keyboard(self):
        input_manager = activity.getSystemService(Context.INPUT_METHOD_SERVICE)
        view = PythonActivity.mView
        input_manager.showSoftInput(view, InputMethodManager.SHOW_FORCED)

    def _hide_keyboard(self):
        input_manager = activity.getSystemService(Context.INPUT_METHOD_SERVICE)
        view = PythonActivity.mView
        input_manager.hideSoftInputFromWindow(view.getWindowToken(), 0)

    def _is_connection(self):
        service = Context.CONNECTIVITY_SERVICE
        connection_manager = activity.getSystemService(service)
        active_network = connection_manager.getActiveNetworkInfo()
        return active_network is not None and active_network.isConnected()


def instance():
    return AndroidUtils()
