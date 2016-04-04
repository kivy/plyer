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
                     CArray, objc_dict, objc_i)
from pyobjus.objc_py_types import enum

CBCentralManager = CBCentralManagerState = cb_central_manager_state_map = None

def _init():
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

    cb_central_manager_state_map = {v:k.replace('_', ' ') for k, v
                                    in CBCentralManagerState.__dict__.items()
                                    if not k.startswith('_')}

c = CArray()

NSMutableArray = autoclass('NSMutableArray')

central_manager = None
central_impl = None

# from os.path import dirname, join
# make_dylib(join(dirname(__file__), 'libs', 'cbcentral.m'), frameworks=['Foundation', 'CoreBluetooth'])
# load_dylib(join(dirname(__file__), 'libs', 'cbcentral.dylib'))
# cbcentral = autoclass('cbcentral')


class BleDevice(BleCentral.Device):
    def __init__(self, uuid, name, power, announcement=None, services=None,
                 peripheral=None):
        super(BleDevice, self).__init__(uuid, name, power,
                                        announcement=announcement,
                                        services=services)
        self.peripheral = peripheral

    @property
    def key(self):
        return self.peripheral

    def _update(self, new):
        self.peripheral = new.peripheral
        self.uuid = UUID(iprop(self.peripheral.identifier).UUIDString().cString())
        self.name = iprop(self.peripheral.name).cString()
        super(BleDevice, self)._update(new)

    def _connect(self, on_connect=None, on_disconnect=None):
        central_impl.connect(self, on_connect, on_disconnect)

    def _disconnect(self, callback=None):
        central_impl.disconnect(self, callback)


class BleCentralImpl(object):
    def __init__(self):
        global central_manager, central_impl
        _init()
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

        print('found peripheral:', peripheral)
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
        if self.connect_to and self.connect_to.peripheral == peripheral:
            if self.connect_callback:
                self.connect_callback(self.connect_to)

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

