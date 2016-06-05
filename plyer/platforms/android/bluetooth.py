'''
Android Bluetooth
-----------
'''

from plyer.facades import Bluetooth
from plyer.platforms.android import activity
from jnius import PythonJavaClass, java_method, autoclass, cast
from jnius import JavaClass, MetaJavaClass
Intent = autoclass('android.content.Intent')
GenericBroadcastReceiver = autoclass(
    'org.renpy.android.GenericBroadcastReceiver')
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
IntentFilter = autoclass('android.content.IntentFilter')
Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')


class AndroidBluetooth(Bluetooth):

    scan_devices = []
    bluetooth_reg = None
    BA = None

    class BroadcastReceiver(PythonJavaClass):

        '''Private class for receiving results from Bluetooth manager.'''
        __javainterfaces__ = [
            'org/renpy/android/GenericBroadcastReceiverCallback'
        ]
        __javacontext__ = 'app'

        def __init__(self, facade, *args, **kwargs):
            PythonJavaClass.__init__(self, *args, **kwargs)
            self.facade = facade

        @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
        def onReceive(self, context, intent):
            scan_devices = []
            action = intent.getAction()
            if (BluetoothAdapter.ACTION_DISCOVERY_STARTED == action):
                pass
            else if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED == action):
                pass
            else if (BluetoothDevice.ACTION_FOUND == action):
                device = cast(BluetoothDevice, intent.getParcableExtra(
                              BluetoothDevice.EXTRA_DEVICE))
                scan_devices.append(device.getName())
            self.facade.scan_devices = scan_devices[:]

    def __init__(self, **kwargs):
        super(AndroidBluetooth, self).__init__(**kwargs)
        self.BA = BluetoothAdapter.getDefaultAdapter()
        self._register_receiver()

    def _on_resume(self):
        self._register_receiver()

    def _register_receiver(self):
        broadcast_receiver = AndroidBluetooth.BroadcastReceiver(self)
        self.bluetooth_reg = GenericBroadcastReceiver(broadcast_receiver)

        self.intent_filter = IntentFilter()
        self.intent_filter.addAction(BluetoothAdapter.ACTION_STATE_CHANGED)
        self.intent_filter.addAction(BluetoothDevice.ACTION_FOUND)
        self.intent_filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_STARTED)
        self.intent_filter.addAction(
                           BluetoothAdapter.ACTION_DISCOVERY_FINISHED)
        activity.registerReceiver(self.bluetooth_reg, self.intent_filter)

    def _on_pause(self):
        activity.unregisterReceiver(self.bluetooth_reg)

    def _enable(self):
        if not self.BA.isEnabled():
            intent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            activity.startActivityForResult(intent, 0)

    def _is_enabled(self):
        return self.BA.isEnabled()

    def _disable(self):
        if self.BA.isEnabled():
            self.BA.disable()

    def _visible(self):
        intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
        activity.startActivityForResult(intent, 1)

    def _start_discovery(self):
        self.BA.startDiscovery()

    def _get_scan_devices(self):
        return self.scan_devices

    def _get_paired_devices(self):
        return self.BA.getBoundedDevices()


def instance():
    return AndroidBluetooth()
