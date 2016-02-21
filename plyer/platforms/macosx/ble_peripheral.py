'''
MacOSX BLE Peripheral
---------------------


'''
from uuid import UUID
from os.path import dirname, join

from plyer.facades import BlePeripheral
from plyer.utils import iprop
from plyer.platforms.macosx.libs.cbadvertisement import CBAdvertisementDataKeys

from pyobjus import (autoclass, protocol, CArray, objc_dict, objc_arr)
from pyobjus.dylib_manager import load_framework
from pyobjus.objc_py_types import enum

load_framework('/System/Library/Frameworks/CoreBluetooth.framework')

CBPeripheralManager = autoclass('CBPeripheralManager')
CBMutableService = autoclass('CBMutableService')
CBMutableCharacteristic = autoclass('CBMutableCharacteristic')
CBUUID = autoclass('CBUUID')

CBPeripheralManagerState = enum('CBPeripheralManagerState',
                                unknown=0,
                                resetting=1,
                                unsupported=2,
                                unauthorized=3,
                                powered_off=4,
                                powered_on=5)

cb_peripheral_manager_state_map = {v:k.replace('_', ' ') for k, v
                                   in CBPeripheralManagerState.__dict__.items()
                                   if not k.startswith('_')}


class BlePeripheralService(BlePeripheral.Service):
    cbuuid = None
    service = None

    def init(self):
        self.cbuuid = CBUUID.UUIDWithString_(str(self.uuid))
        cbms = CBMutableService.alloc()
        self.service = cbms.initWithType_primary_(self.cbuuid, self.primary)


class BlePeripheralCharacteristic(BlePeripheral.Characteristic):
    pass


class BlePeripheralImpl(object):
    def __init__(self):
        self.state = 0
        self.on_state = None
        self.on_service_added = None
        self.on_service_error = None
        self.on_advertising_started = None
        self.on_advertising_error = None
        self.services = {}
        self.pending_services = {}
        self.peripheral = CBPeripheralManager.alloc()
        self.peripheral.initWithDelegate_queue_options_(self, None, None)

    @property
    def state_description(self):
        return cb_peripheral_manager_state_map[self.state]

    @property
    def bt_on(self):
        return self.state == CBPeripheralManagerState.powered_on

    @property
    def advertising(self):
        return self.peripheral.isAdvertising

    @protocol('CBPeripheralManagerDelegate')
    def peripheralManagerDidUpdateState_(self, peripheral):
        self.state = iprop(peripheral.state)

        if callable(self.on_state):
            self.on_state(self.state_description)

    def add_service(self, service):
        assert isinstance(service, BlePeripheralService)
        self.pending_services[service.uuid] = service
        self.peripheral.addService_(service.service)

    @protocol('CBPeripheralManagerDelegate')
    def peripheralManager_didAddService_error_(self, peripheral, service,
                                               error):
        uuid = UUID(iprop(service.UUID).UUIDString.cString())
        pending_service = self.pending_services.get(uuid, None)
        if pending_service:
            del self.pending_services[uuid]
        running_service = self.services.get(uuid, None)
        pyservice = running_service or pending_service or None

        if error:
            if running_service:
                del self.services[uuid]
            if callable(self.on_service_error):
                desc = error.localizedDescription
                if callable(desc):
                    desc = desc()
                self.on_service_error(pyservice, desc)
        else:
            if pyservice:
                self.services[uuid] = pyservice
            if callable(self.on_service_added):
                self.on_service_added(pyservice)

    def start_advertising(self, name):
        servarray = objc_arr(*[iprop(s.service.UUID) for s in self.services.values()])

        data = objc_dict({
            CBAdvertisementDataKeys.LocalName: name,
            CBAdvertisementDataKeys.ServiceUUIDs: servarray
        })

        self.peripheral.startAdvertising_(data)

    def stop_advertising(self):
        self.peripheral.stopAdvertising()

    @protocol('CBPeripheralManagerDelegate')
    def peripheralManagerDidStartAdvertising_error_(self, peripheral, error):
        if error:
            if callable(self.on_advertising_error):
                desc = error.localizedDescription
                if callable(desc):
                    desc = desc()
                self.on_advertising_error(desc)
        else:
            if callable(self.on_advertising_started):
                self.on_advertising_started()


class OSXBlePeripheral(BlePeripheral):
    Characteristic = BlePeripheralCharacteristic
    Service = BlePeripheralService

    _ble = None

    @property
    def ble(self):
        if not self._ble:
            self.init()
        return self._ble

    def init(self):
        self._ble = BlePeripheralImpl()

    def _state(self):
        return self.ble.state_description

    def _has_ble(self):
        return self.ble.bt_on

    def _is_advertising(self):
        return self.ble.advertising

    def _add_service(self, service):
        self.ble.add_service(service)

    def _start_advertising(self, name):
        self.ble.start_advertising(name)

    def _stop_advertising(self):
        self.ble.stop_advertising()

    def set_callbacks(self, **kwargs):
        super(OSXBlePeripheral, self).set_callbacks(**kwargs)
        self.ble.on_state = self.on_state
        self.ble.on_service_added = self.on_service_added
        self.ble.on_service_error = self.on_service_error
        self.ble.on_advertising_started = self.on_advertising_started
        self.ble.on_advertising_error = self.on_advertising_error


def instance():
    return OSXBlePeripheral()

