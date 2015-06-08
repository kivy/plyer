from jnius import autoclass
from jnius import cast
from jnius import java_method
from jnius import PythonJavaClass

from mwifi import Wifi
from plyer.platforms.android import activity

Context = autoclass('android.content.Context')
GenericBroadcastReceiver = autoclass(
    'org.renpy.android.GenericBroadcastReceiver'
)
Intent = autoclass('android.content.Intent')
IntentFilter = autoclass('android.content.IntentFilter')
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Sensor = autoclass('android.hardware.Sensor')
WifiManager = autoclass('android.net.wifi.WifiManager')


class AndroidWifi(Wifi):
    '''Android Wifi implementation.

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

        def __init__(self, facade, *args, **kwargs):
            PythonJavaClass.__init__(self, *args, **kwargs)
            self.facade = facade

        @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
        def onReceive(self, context, intent):
            '''Receive list of available access points from wifi and saves
            this list in `scanned_results`.

            :param context: our activity
            '''
            wifi_service = context.getSystemService(Context.WIFI_SERVICE)
            wifi_manager = cast('android.net.wifi.WifiManager', wifi_service)
            self.facade.scanned_results = wifi_manager.getScanResults()

    def __init__(self):
        super(AndroidWifi, self).__init__()
        wifi_service = activity.getSystemService(Context.WIFI_SERVICE)
        self.wifi_manager = cast('android.net.wifi.WifiManager', wifi_service)

    def _enable(self):
        broadcast_receiver = AndroidWifi.BroadcastReceiver(self)
        self.wifi_scanner = GenericBroadcastReceiver(broadcast_receiver)
        intent_filter = IntentFilter()
        intent_filter.addAction(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION)
        activity.registerReceiver(self.wifi_scanner, intent_filter)

    def _is_enabled(self):
        return self.wifi_manager and self.wifi_manager.isWifiEnabled()

    def _disable(self):
        activity.unregisterReceiver(self.wifi_scanner)

    def _get_access_points(self):
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
        return access_points[:]

    def _start_scanning(self):
        self.wifi_manager.startScan()


def instance():
    return AndroidWifi()
