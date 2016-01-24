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

    class BroadcastReceiver(PythonJavaClass):

        '''Private class for receiving results from Bluetooth manager.'''
        __javainterfaces__ = [
            'org/renpy/android/GenericBroadcastReceiverCallback'
        ]
        __javacontext__ = 'app'

        def __init__(self, facade, *args, **kwargs):
            PythonJavaClass.__init__(self, *args, **kwargs)
            self.facade = facade

    def __init__(self, **kwargs):
        super(AndroidBluetooth, self).__init__(**kwargs)
        self.BA = BluetoothAdapter.getDefaultAdapter()
        self.filter = IntentFilter()
        self.filter.addAction(BluetoothAdapter.ACTION_STATE_CHANGED)
        self.filter.addAction(BluetoothDevice.ACTION_FOUND)
        self.filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_STARTED)
        self.filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED)
        broadcast_receiver = AndroidBluetooth.BroadcastReceiver(self)
        self.bluetooth_reg = GenericBroadcastReceiver(broadcast_receiver)
        activity.registerReceiver(self.bluetooth_reg, self.filter)

    @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
    def onReceive(self, context, intent):
        action = intent.getAction()
        # Do something in future for filters

    def _on_pause(self):
        activity.unregisterReceiver(self.bluetooth_reg)

    def _on_resume(self):
        activity.registerReceiver(self.bluetooth_reg, self.filter)

    def _on_stop(self):
        activity.unregisterReceiver(self.bluetooth_reg)

    def _start(self):
        if not self.BA.isEnabled():
            intent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            activity.startActivityForResult(intent, 0)
        else:
            pass

    def _stop(self):
        self.BA.disable()

    def _visible(self):
        intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
        activity.startActivityForResult(intent, 1)


def instance():
    return AndroidBluetooth()
