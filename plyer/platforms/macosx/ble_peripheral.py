'''
MacOSX BLE Peripheral
---------------------


'''
from uuid import UUID
from os.path import dirname, join

from plyer.facades import BlePeripheral
from plyer.utils import iprop

from pyobjus import (autoclass, protocol, CArray, objc_dict, objc_arr)
from pyobjus.dylib_manager import load_framework
from pyobjus.objc_py_types import enum
from pyobjus.consts.corebluetooth import CBAdvertisementDataKeys

load_framework('/System/Library/Frameworks/CoreBluetooth.framework')

NSData = autoclass('NSData')
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

c = CArray()

peripheral_manager = None


class BlePeripheralService(BlePeripheral.Service):
    cbuuid = None
    service = None
    characteristics = None

    def init(self):
        self.cbuuid = CBUUID.UUIDWithString_(str(self.uuid))
        self.service = CBMutableService.alloc()
        self.service.initWithType_primary_(self.cbuuid, self.primary)

    def _add_characteristic(self, characteristic):
        chars = self.characteristics or {}
        chars[characteristic.characteristic] = characteristic
        characteristic.service = self
        self.characteristics = chars
        self.service.characteristics = objc_arr(
            *self.characteristics.keys())


class BlePeripheralCharacteristic(BlePeripheral.Characteristic):
    cbuuid = None
    characteristic = None
    service = None

    def init(self):
        self.cbuuid = CBUUID.UUIDWithString_(str(self.uuid))
        self.characteristic = CBMutableCharacteristic.alloc()
        self.characteristic.initWithType_properties_value_permissions_(
            self.cbuuid, self.properties, None, self.permissions
        )

    def set_value(self, value):
        self.value = value
        data = self.create_data(value)
        peripheral_manager.updateValue_forCharacteristic_onSubscribedCentrals_(
            data, self.characteristic, None
        )
        return data

    def create_data(self, value):
        if value is None:
            return value
        assert isinstance(value, (bytes, bytearray))
        data = NSData.dataWithBytes_length_(value, len(value))
        return data


class BlePeripheralImpl(object):
    def __init__(self):
        global peripheral_manager
        self.state = 0
        self.on_state = None
        self.on_service_added = None
        self.on_service_error = None
        self.on_advertising_started = None
        self.on_advertising_error = None
        self.on_characteristic_subscribed = None
        self.on_characteristic_write = None
        self.services = {}
        self.pending_services = {}
        self.peripheral = peripheral_manager = CBPeripheralManager.alloc()
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

    def remove_service(self, service):
        uuid = service.uuid
        if uuid in self.pending_services:
            del self.pending_services[uuid]
        if uuid in self.services:
            del self.services[uuid]
        peripheral_manager.removeService_(service.service)

    def remove_all_services(self):
        peripheral_manager.removeAllServices()

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

    @protocol('CBPeripheralManagerDelegate')
    def peripheralManager_didReceiveReadRequest_(self, peripheral, request):
        uuid = iprop(request.characteristic.UUID)
        for service in self.services.values():
            for char in service.characteristics.values():
                if iprop(char.characteristic.UUID).isEqual_(uuid):
                    if char.value:
                        if callable(char.on_read_request):
                            char.on_read_request(char)
                        data = char.create_data(char.value)
                        request.value = data
                        peripheral.respondToRequest_withResult_(request, 0)
                        if callable(char.on_read):
                            char.on_read(char)
                        return

    @protocol('CBPeripheralManagerDelegate')
    def peripheralManager_didReceiveWriteRequests_(self, peripheral, requests):
        for i in range(requests.count()):
            request = requests.objectAtIndex_(i)
            self.respond_to_write_request(peripheral, request)

    def respond_to_write_request(self, peripheral, request):
        uuid = iprop(request.characteristic.UUID)
        for service in self.services.values():
            for char in service.characteristics.values():
                if iprop(char.characteristic.UUID).isEqual_(uuid):
                    value = request.value
                    length = value.length()
                    if length:
                        char.value = bytearray(c.get_from_ptr(iprop(value.bytes).arg_ref, 'C', length))
                    else:
                        char.value = None

                    peripheral.respondToRequest_withResult_(request, 0)

                    if callable(char.on_write):
                        char.on_write(char)
                    if callable(self.on_characteristic_write):
                        self.on_characteristic_write(service, char)
                    return

        peripheral.respondToRequest_withResult_(request, 0x0a)  # attribute not found

    @protocol('CBPeripheralManagerDelegate')
    def peripheralManager_central_didSubscribeToCharacteristic_(self,
            peripheral, central, characteristic):
        if callable(self.on_characteristic_subscribed):
            for service in self.services.values():
                char = service.characteristics.get(characteristic)
                if char:
                    if callable(char.on_subscribe):
                        char.on_subscribe(char)
                    if callable(self.on_characteristic_subscribed):
                        self.on_characteristic_subscribed(service, char)
                    return

    def start_advertising(self, name):
        services = [iprop(s.service.UUID) for s in self.pending_services.values()]
        servarray = objc_arr(*services) if services else None

        adv_dict = {CBAdvertisementDataKeys.LocalName: name}
        if servarray:
            adv_dict[CBAdvertisementDataKeys.ServiceUUIDs] = servarray
        data = objc_dict(adv_dict)

        self.peripheral.startAdvertising_(data)
        for service in self.pending_services.values():
            self.peripheral.addService_(service.service)

    def stop_advertising(self):
        self.peripheral.stopAdvertising()

    @protocol('CBPeripheralManagerDelegate')
    def peripheralManagerDidStartAdvertising_error_(self, peripheral, error):
        if error:
            if callable(self.on_advertising_error):
                desc = iprop(error.localizedDescription).cString()
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

    def _remove_service(self, service):
        self.ble.remove_service(service)

    def _remove_all_services(self):
        self.ble.remove_all_services()

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
        self.ble.on_characteristic_subscribed = self.on_characteristic_subscribed
        self.ble.on_characteristic_write = self.on_characteristic_write


def instance():
    return OSXBlePeripheral()

