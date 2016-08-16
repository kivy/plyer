'''
MacOSX BLE Central
------------------


'''
from __future__ import print_function

import traceback
from threading import Thread
from time import sleep
from uuid import UUID

from plyer.facades import BleCentral
from pyobjus.consts.corebluetooth import CBAdvertisementDataKeys
from plyer.utils import iprop

from pyobjus.dylib_manager import load_framework, make_dylib, load_dylib, INCLUDE
from pyobjus import (autoclass, protocol, symbol, dereference, ObjcString,
                     CArray, objc_dict, objc_i, objc_str)
from pyobjus.objc_py_types import enum

global CBCentralManager, CBCentralManagerState, cb_central_manager_state_map
load_framework('/System/Library/Frameworks/CoreBluetooth.framework')
# load_framework(INCLUDE.IOBluetooth)

CBCentralManager = autoclass('CBCentralManager')

CBCentralManagerState = enum('CBCentralManagerState',
                             unknown=0,
                             resetting=1,
                             unsupported=2,
                             unauthorized=3,
                             powered_off=4,
                             powered_on=5)

CBUUID = autoclass('CBUUID')

cb_central_manager_state_map = {v:k.replace('_', ' ') for k, v
                                in CBCentralManagerState.__dict__.items()
                                if not k.startswith('_')}

c = CArray()

NSMutableArray = autoclass('NSMutableArray')
NSData = autoclass('NSData')
NSString = autoclass('NSString')

central_manager = None
central_impl = None

# from os.path import dirname, join
# make_dylib(join(dirname(__file__), 'libs', 'cbcentral.m'), frameworks=['Foundation', 'CoreBluetooth'])
# load_dylib(join(dirname(__file__), 'libs', 'cbcentral.dylib'))
# cbcentral = autoclass('cbcentral')


def uuid_to_cbuuid(uuid):
    return CBUUID.UUIDWithString_(str(uuid))


def cbuuid_to_uuid(cbuuid):
    uuid_string = iprop(iprop(cbuuid).UUIDString).cString()
    if len(uuid_string) == 4:
        uuid_string = '0000' + uuid_string + '-0000-1000-8000-00805F9B34FB'
    return UUID(uuid_string)


class BleCharacteristic(BleCentral.Characteristic):
    def __init__(self, uuid, service, characteristic):
        properties = iprop(characteristic.properties)
        super(BleCharacteristic, self).__init__(uuid, service, properties)
        self.characteristic = characteristic
        self.on_read = None

    def _read(self, on_read=None):
        self.on_read = on_read
        self.service.service.peripheral.readValueForCharacteristic_(self.characteristic)

    def _write(self, value, on_write=None):
        self.on_write = on_write
        # data = NSData.dataWithBytes_length_(value, len(value))
        # ostr = objc_str(value)
        # data = ostr.dataWithEncoding_(1)
        # ostr = NSString.stringWithCString_encoding_(value, 1)
        # data = ostr.dataUsingEncoding()
        self.value = value
        data = NSData.dataWithBytes_length_(value, len(value))
        type_ = int(not bool(on_write))
        # print('connected', iprop(self.service.service.peripheral.state))
        print('write', self.uuid, 'value', repr(value), 'length', data.length(), 'type', type_)
        self.service.service.peripheral.writeValue_forCharacteristic_type_(data, self.characteristic, type_)


class BleService(BleCentral.Service):
    def __init__(self, uuid, service):
        super(BleService, self).__init__(uuid)
        self.service = service
        self.on_discover = None

    def _discover_characteristics(self, uuids=None, on_discover=None):
        print('discover characteristics', self.uuid, uuids)
        if uuids:
            uuids = [uuid_to_cbuuid(u) for u in uuids]
        self.on_discover = on_discover
        self.service.peripheral.discoverCharacteristics_forService_(uuids, self.service)


class BleDevice(BleCentral.Device):
    def __init__(self, uuid, name, power, announcement=None, services=None,
                 peripheral=None):
        super(BleDevice, self).__init__(uuid, name, power,
                                        announcement=announcement,
                                        services=services)
        self.peripheral = peripheral
        self.on_discover = None

    @property
    def key(self):
        return self.peripheral

    def _update(self, new):
        self.peripheral = new.peripheral
        # self.uuid = UUID(iprop(self.peripheral.identifier).UUIDString().cString())
        self.uuid = cbuuid_to_uuid(self.peripheral.identifier)
        self.name = iprop(self.peripheral.name).cString()
        super(BleDevice, self)._update(new)

    def _connect(self, on_connect=None, on_disconnect=None):
        print('set delegate')
        self.peripheral.setDelegate_(self)
        central_impl.connect(self, on_connect, on_disconnect)

    def _disconnect(self, callback=None):
        central_impl.disconnect(self, callback)

    def _discover_services(self, uuids=None, on_discover=None):
        print('discover services:', uuids)
        if uuids:
            # uuids = [CBUUID.UUIDWithString_(str(u)) for u in uuids]
            uuids = [uuid_to_cbuuid(u) for u in uuids]
        self.on_discover = on_discover
        print('set delegate')
        self.peripheral.setDelegate_(self)
        print('call discoverServices_')
        self.peripheral.discoverServices_(uuids)
        print('done')

    @protocol('CBPeripheralDelegate')
    def peripheral_didDiscoverServices_(self, peripheral, error):
        print('did discover services')
        if peripheral == self.peripheral:
            print(' is my peripheral')
            services = {}
            if not error:
                iservices = iprop(peripheral.services)
                count = iprop(iservices.count)
                print(' found', count, 'services')
                for i in range(count):
                    iservice = iservices.objectAtIndex_(i)
                    # uuid_string = iprop(iprop(iservice.UUID).UUIDString).cString()
                    # if len(uuid_string) == 4:
                    #     uuid_string = '0000' + uuid_string + '-0000-1000-8000-00805F9B34FB'
                    # uuid = UUID(uuid_string)
                    uuid = cbuuid_to_uuid(iservice.UUID)
                    print('  ', uuid)
                    service = BleService(uuid, iservice)
                    self.services[uuid] = service
                    services[uuid] = service
            else:
                error = iprop(error.localizedDescription)
                print('error:', error)
            if callable(self.on_discover):
                self.on_discover(services, error)

    @protocol('CBPeripheralDelegate')
    def peripheral_didDiscoverCharacteristicsForService_error_(self, peripheral, iservice, error):
        print('did discover characteristics')
        if error:
            error = iprop(error.localizedDescription)
            print('error:', error)
        if peripheral == self.peripheral:
            print(' is my peripheral')
            for service in self.services.values():
                if service.service == iservice:
                    print(' found service', service)
                    characteristics = {}
                    if not error:
                        icharacteristics = iprop(iservice.characteristics)
                        count = iprop(icharacteristics.count)
                        print(' found', count, 'characteristics')
                        for i in range(count):
                            icharacteristic = icharacteristics.objectAtIndex_(i)
                            uuid = cbuuid_to_uuid(icharacteristic.UUID)
                            print('  ', uuid)
                            characteristic = BleCharacteristic(uuid, service, icharacteristic)
                            service.characteristics[uuid] = characteristic
                            characteristics[uuid] = characteristic
                    if callable(service.on_discover):
                        service.on_discover(characteristics, error)
                    return

    @protocol('CBPeripheralDelegate')
    def peripheral_didUpdateValueForCharacteristic_error_(self, peripheral, characteristic, error):
        print('did update value for characteristic')
        if error:
            error = iprop(error.localizedDescription)
            print('error:', error)
        if peripheral == self.peripheral:
            print(' is my peripheral')
            for service in self.services.values():
                if service.service == iprop(characteristic.service):
                    print(' found service', service)
                    for char in service.characteristics.values():
                        if char.characteristic == characteristic:
                            print(' found characteristic', char)
                            if not error:
                                value = iprop(characteristic.value)
                                ref = iprop(value.bytes).arg_ref
                                length = iprop(value.length)
                                if length:
                                    char.value = bytearray(c.get_from_ptr(ref, 'C', length))
                                else:
                                    char.value = None
                            if callable(char.on_read):
                                char.on_read(char, error)
                            return
                    return

    @protocol('CBPeripheralDelegate')
    def peripheral_didWriteValueForCharacteristic_error_(self, peripheral, characteristic, error):
        print('did write value for characteristic')
        if error:
            error = iprop(error.localizedDescription)
            print('error:', error)
        if peripheral == self.peripheral:
            print(' is my peripheral')
            for service in self.services.values():
                if service.service == iprop(characteristic.service):
                    print(' found service', service)
                    for char in service.characteristics.values():
                        if char.characteristic == characteristic:
                            print(' found characteristic', char)
                            if callable(char.on_write):
                                char.on_write(char, error)
                            return
                    return


class BleCentralImpl(object):
    def __init__(self):
        global central_manager, central_impl
        central_impl = self
        self.state = 0
        self.scanning = False
        self.connecting = False
        self.connect_to = None
        self.connect_callback = None
        self.disconnect_callback = None
        self.on_state = None
        self.on_discover = None
        self.peripherals = set()
        self.central = central_manager = CBCentralManager.alloc().initWithDelegate_queue_(self, None)
        # cb = cbcentral.alloc().init()
        # cb.initCentralQueue_delegate_(self.central, self)
        # self.central.initWithDelegate_queue_(self, None)
        # self.central = cb.centralWithQueue_(self)
        # self.cbcentral = cbcentral.alloc().init()

        # self._peripherals = NSMutableArray.alloc().init()

        # self.cbthread = Thread(target=self.query_cbcentral)
        # self.cbthread.setDaemon(True)
        # self.cbthread.start()

    def query_cbcentral(self):
        while True:
            while self.cbcentral.hasEvents():
                oevent = self.cbcentral.getEvent()
                event = [oevent.objectAtIndex_(i) for i in range(iprop(oevent.count))]
                event[0] = iprop(event[0].cString)
                print('received event:', event)
                try:
                    getattr(self, event[0])(*event[1:])
                except Exception as e:
                    print('bad event:', e)
                    traceback.print_exc()
            sleep(0.1)

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

        # print('found peripheral:', peripheral)
        # peripheral.retain()
        # print('retained')
        # cbcentral.addPeripheral_(peripheral)
        # if not self._peripherals.containsObject_(peripheral):
        #     self._peripherals.addObject_(peripheral)
        #     print('stored peripheral:', peripheral)
        self.peripherals.add(peripheral)
        device = self.device_from_advertisement(peripheral, advertisementData, power)
        # peripheral.setDelegate_(self)
        # print('set delegate for', peripheral, device)

        if device and callable(self.on_discover):
            self.on_discover(device)

    def device_from_advertisement(self, peripheral, advertisementData, power):
        try:
            uuid = iprop(peripheral.identifier).UUIDString().cString()
            name = iprop(peripheral.name).cString()
        except Exception:
            return

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

    def start_scanning(self, allow_duplicates=True):
        if self.scanning:
            return

        print('allow duplicates:', allow_duplicates)
        options = objc_dict({
            'kCBScanOptionAllowDuplicates': objc_i(int(allow_duplicates))
        })
        self.central.scanForPeripheralsWithServices_options_(None, options)
        # self.cbcentral.startScanning_(allow_duplicates)
        self.scanning = True

    def stop_scanning(self):
        if not self.scanning:
            return

        self.central.stopScan()
        # self.cbcentral.stopScan()
        self.scanning = False

    def connect(self, device, on_connect=None, on_disconnect=None):
        print('connect:', device)
        if self.connect_to:
            self.disconnect(self.connect_to)
        self.connect_to = device
        self.connect_callback = on_connect
        self.disconnect_callback = on_disconnect

        # ct = Thread(target=self.connect_thread)
        # ct.setDaemon(True)
        # ct.start()
        # self.cbcentral.connectPeripheral_(self.connect_to.peripheral)
        self.central.cancelPeripheralConnection_(device.peripheral)
        self.central.connectPeripheral_options_(device.peripheral, None)

    # def connect_thread(self):
    #     print('connect thread started')
    #     # options = objc_dict({
    #     #     CBConnectPeripheralOptionKeys.NotifyOnConnection: objc_i(1),
    #     #     CBConnectPeripheralOptionKeys.NotifyOnDisconnection: objc_i(1),
    #     #     CBConnectPeripheralOptionKeys.NotifyOnNotification: objc_i(1),
    #     # })
    #     # self.central.connectPeripheral_options_(self.connect_to.peripheral, None)
    #     self.cbcentral.connectPeripheral_(self.connect_to.peripheral)
    #     self.connecting = True
    #     save = objc_dict({'save': self.connect_to.peripheral})
    #     while self.connecting:
    #         print('waiting...')
    #         sleep(0.1)
    #     print('connected!')

    def disconnect(self, device, callback=None):
        print('disconnect:', device)
        if callable(callback):
            self.disconnect_callback = callback
        self.central.cancelPeripheralConnection_(device.peripheral)
        # self.cbcentral.cancelConnectPeripheral_(device.peripheral)

    @protocol('CBCentralManagerDelegate')
    def centralManager_didConnectPeripheral_(self, central, peripheral):
        print('did connect peripheral')
        self.connecting = False
        device = self.connect_to
        if device and device.peripheral == peripheral:
            print('set delegate')
            peripheral.setDelegate_(device)
            if iprop(peripheral.services):
                device.peripheral_didDiscoverServices_(peripheral, None)
            if self.connect_callback:
                self.connect_callback(device)

    @protocol('CBCentralManagerDelegate')
    def centralManager_didFailToConnectPeripheral_error_(self, central,
                                                         peripheral, error):
        print('did fail to connect peripheral')
        self.connecting = False
        if self.connect_to and self.connect_to.peripheral == peripheral:
            if callable(self.connect_callback):
                self.connect_callback(self.connect_to, iprop(error.localizedDescription))

    @protocol('CBCentralManagerDelegate')
    def centralManager_didDisconnectPeripheral_error_(self, central, peripheral, error):
        print('did disconnect peripheral')
        self.connecting = False
        if self.connect_to and self.connect_to.peripheral == peripheral:
            if callable(self.disconnect_callback):
                errstr = iprop(error.localizedDescription) if error else None
                self.disconnect_callback(self.connect_to, errstr)


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

    def _start_scanning(self, allow_duplicates=True):
        if self.ble.bt_on:
            self.ble.start_scanning(allow_duplicates)

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

