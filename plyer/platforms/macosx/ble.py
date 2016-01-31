'''
MacOSX Bluetooth
----------------


'''

from plyer.facades import Ble

from pyobjus.dylib_manager import load_framework
from pyobjus import autoclass, protocol, dereference, ObjcString, CArray
from pyobjus.objc_py_types import enum, dict_from_objc

load_framework('/System/Library/Frameworks/CoreBluetooth.framework')

CBCentralManager = autoclass('CBCentralManager')

CBCentralManagerState = enum('CBCentralManagerState',
                             unknown=0,
                             resetting=1,
                             unsupported=2,
                             unauthorized=3,
                             powered_off=4,
                             powered_on=5)

cb_central_manager_state_map = {v:k.replace('_', ' ') for k, v
                                in CBCentralManagerState.__dict__.items()
                                if not k.startswith('_')}


class _BleImpl(object):
    def __init__(self):
        self.state = 0
        self.scanning = False
        self.on_state = None
        self.on_discover = None
        self.central = CBCentralManager.alloc()
        self.central.initWithDelegate_queue_(self, None)

    @property
    def state_description(self):
        return cb_central_manager_state_map[self.state]

    @property
    def bt_on(self):
        return self.state == CBCentralManagerState.powered_on

    @protocol('CBCentralManagerDelegate')
    def centralManagerDidUpdateState_(self, central):
        self.state = central.state
        # print 'central state updated: {}[{}]'.format(self.state_description, self.state)

        if self.scanning and not self.bt_on:
            self.stop_scanning()

        if callable(self.on_state):
            self.on_state(self.state_description)

    @protocol('CBCentralManagerDelegate')
    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self,
            central, peripheral, advertisementData, RSSI):
        power = RSSI.floatValue()

        data = dict_from_objc(advertisementData)
        advdata = data['kCBAdvDataManufacturerData']
        advbytes = advdata.bytes()
        advbytes.of_type = 'C'
        announcement = dereference(advbytes, of_type=CArray, return_count=advdata.length())

        if callable(self.on_discover):
            self.on_discover(Ble.Device(announcement, power))

    def start_scanning(self):
        if self.scanning:
            print 'already scanning'
            return

        print 'start scanning'
        self.central.scanForPeripheralsWithServices_options_(None, None)
        self.scanning = True

    def stop_scanning(self):
        if not self.scanning:
            print 'not scanning'
            return

        print 'stop scanning'
        self.central.stopScan()
        self.scanning = False


class OSXBle(Ble):

    _ble = None

    @property
    def ble(self):
        if not self._ble:
            self.init()
        return self._ble

    def __init__(self):
        self._ble = _BleImpl()

    def _state(self):
        return self.ble.state_description

    def _has_ble(self):
        return self.ble.bt_on

    def _start_scanning(self):
        if self.ble.bt_on:
            self.ble.start_scanning()

    def _stop_scanning(self):
        if self.ble.bt_on:
            self.ble.stop_scanning()

    def _is_scanning(self):
        return self.ble.scanning

    def set_callbacks(self, **kwargs):
        super(OSXBle, self).set_callbacks(**kwargs)
        self.ble.on_state = self.on_state
        self.ble.on_discover = self.on_discover


def instance():
    return OSXBle()
