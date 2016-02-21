'''
MacOSX BLE Central
------------------


'''

from plyer.facades import BleCentral
from plyer.platforms.macosx.libs.cbadvertisement import CBAdvertisementDataKeys
from plyer.utils import iprop

from pyobjus.dylib_manager import load_framework
from pyobjus import (autoclass, protocol, symbol, dereference, ObjcString,
                     CArray, objc_dict, objc_i)
from pyobjus.objc_py_types import enum

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

c = CArray()


class BleDevice(BleCentral.Device):
    def __init__(self, uuid, name, power, announcement=None, services=None,
                 peripheral=None):
        super(BleDevice, self).__init__(uuid, name, power,
                                        announcement=announcement,
                                        services=services)
        self.peripheral = peripheral

    def _update(self, new):
        super(BleDevice, self)._update(new)
        self.peripheral = new.peripheral


class BleCentralImpl(object):
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
        self.state = iprop(central.state)

        if self.scanning and not self.bt_on:
            self.stop_scanning()

        if callable(self.on_state):
            self.on_state(self.state_description)

    @protocol('CBCentralManagerDelegate')
    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self,
            central, peripheral, advertisementData, RSSI):
        power = RSSI.floatValue()

        device = self.device_from_advertisement(peripheral, advertisementData, power)

        if device and callable(self.on_discover):
            self.on_discover(device)

    def device_from_advertisement(self, peripheral, advertisementData, power):
        uuid = iprop(peripheral.identifier).UUIDString().cString()
        name = iprop(peripheral.name).cString()

        data = advertisementData.objectForKey_(
            CBAdvertisementDataKeys.ManufacturerData)
        if data:
            announcement = c.get_from_ptr(data.bytes().arg_ref, 'C', data.length())
            return BleDevice(uuid, name, power, announcement=announcement,
                             peripheral=peripheral)

        uuids = advertisementData.objectForKey_(
            CBAdvertisementDataKeys.ServiceUUIDs)
        if uuids:
            services = []
            for i in range(iprop(uuids.count)):
                cbuuid = uuids.objectAtIndex_(i)
                services.append(iprop(cbuuid.UUIDString).cString())
            return BleDevice(uuid, name, power, services=services,
                             peripheral=peripheral)

        return None

    def start_scanning(self):
        if self.scanning:
            return

        options = objc_dict({
            'kCBScanOptionAllowDuplicates': objc_i(1)
        })
        self.central.scanForPeripheralsWithServices_options_(None, options)
        self.scanning = True

    def stop_scanning(self):
        if not self.scanning:
            return

        self.central.stopScan()
        self.scanning = False


class OSXBleCentral(BleCentral):

    _ble = None

    @property
    def ble(self):
        if not self._ble:
            self.init()
        return self._ble

    def init(self):
        self._ble = BleCentralImpl()

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
        super(OSXBleCentral, self).set_callbacks(**kwargs)
        self.ble.on_state = self.on_state
        self.ble.on_discover = self.on_discover


def instance():
    return OSXBleCentral()

