'''
BLE example
'''
import operator
from uuid import UUID

from kivy.adapters.listadapter import ListAdapter
from kivy.app import App
from kivy.properties import (BooleanProperty, ObjectProperty, StringProperty,
                             NumericProperty, Clock, Logger)
from kivy.uix.stacklayout import StackLayout

from plyer import ble_central, ble_peripheral


class DeviceItem(StackLayout):
    uuid = StringProperty('none')
    name = StringProperty('none')
    beacon = StringProperty('none')
    beacon_type = StringProperty('unknown')
    services = StringProperty('none')
    distance = NumericProperty(0)
    seen = NumericProperty(-1)
    age = NumericProperty(-1)
    odd = BooleanProperty(False)


class BleTestApp(App):
    ble_central_available = BooleanProperty(False)
    central_state = StringProperty('unknown')
    scanning = BooleanProperty(False)

    ble_peripheral_available = BooleanProperty(False)
    peripheral_state = StringProperty('unknown')
    advertising = BooleanProperty(False)

    adapter = ObjectProperty()

    def __init__(self, **kwargs):
        super(BleTestApp, self).__init__(**kwargs)
        self.beacon = None
        self.characteristic = None
        self.adapter = ListAdapter(data=[], cls=DeviceItem,
                                   args_converter=self.device_args_converter)

    @staticmethod
    def device_args_converter(index, obj):
        return {'uuid': str(obj.uuid),
                'name': str(obj.name),
                'beacon': str(obj.beacon_uuid),
                'distance': obj.distance,
                'beacon_type': obj.type or 'unknown',
                'services': str(len(obj.services)) if obj.services else 'none',
                'seen': int(obj.seen),
                'age': int(obj.age),
                'odd': index % 2 == 1}

    def on_start(self):
        ble_central.init()
        ble_peripheral.init()
        ble_central.set_callbacks(on_state=self.central_state_changed,
                                  on_discover=self.discover)
        ble_peripheral.set_callbacks(on_state=self.peripheral_state_changed,
                                     on_service_added=self.peripheral_service_added,
                                     on_service_error=self.peripheral_service_error,
                                     on_advertising_started=self.peripheral_adv,
                                     on_advertising_error=self.peripheral_adv,
                                     on_characteristic_subscribed=self.char_sub,
                                     on_characteristic_write=self.char_write)
        self.scanning = ble_central.is_scanning
        Clock.schedule_interval(self.update_list, 0.5)

    def toggle_scan(self):
        if ble_central.has_ble:
            if ble_central.is_scanning:
                ble_central.stop_scanning()
                self.scanning = False
            else:
                ble_central.start_scanning()
                self.scanning = True

    def toggle_beacon(self):
        if ble_peripheral.has_ble:
            if ble_peripheral.is_advertising:
                ble_peripheral.stop_advertising()
            else:
                self.start_ble_service()

    def start_ble_service(self):
        uuid = UUID('3F3ED115-0CF8-4252-849B-1114FBDBF9CE')
        read_char_uuid = UUID('DE8F2A9F-CE35-47FD-BDF5-B6B4694202EE')
        write_char_uuid = UUID('EAFB05B5-C27D-495B-B533-95DDC3B26457')
        Char = ble_peripheral.Characteristic
        perms = Char.permission.readable
        props = Char.property.read
        self.read_characteristic = Char(
            read_char_uuid, value=b'a', permissions=Char.permission.readable,
            properties=Char.property.read)
        self.write_characteristic = Char(
            write_char_uuid, permissions=Char.permission.writeable,
            properties=Char.property.write)
        self.beacon = ble_peripheral.Service(uuid)
        self.beacon.add_characteristic(self.read_characteristic)
        self.beacon.add_characteristic(self.write_characteristic)
        ble_peripheral.add_service(self.beacon)
        ble_peripheral.start_advertising()

    def central_state_changed(self, state):
        self.central_state = state
        self.ble_central_available = ble_central.has_ble
        self.scanning = ble_central.is_scanning

    def peripheral_state_changed(self, state):
        self.peripheral_state = state
        self.ble_peripheral_available = ble_peripheral.has_ble
        self.advertising = ble_peripheral.is_advertising

    def peripheral_service_added(self, service):
        Logger.info('Peripheral: service added: {}'.format(service))
        # ble_peripheral.start_advertising()

    def peripheral_service_error(self, service, error):
        Logger.error('Peripheral: service error: {}: {}'.format(error, service))

    def peripheral_adv(self, error=None):
        if error:
            Logger.error('Peripheral: advertisement failed: {}'.format(error))
        else:
            Logger.info('Peripheral: advertising started')
        self.advertising = ble_peripheral.is_advertising

    def char_sub(self, service, characteristic):
        characteristic.set_value(b'boo')

    def char_write(self, service, characteristic):
        Logger.info('Peripheral: write to characteristic: {}'.format(characteristic.value))

    def discover(self, device):
        if device.age < 0.1:
            Logger.info('Central: {}'.format(device))

    def update_list(self, *args):
        self.scanning = ble_central.is_scanning
        self.advertising = ble_peripheral.is_advertising
        devices = sorted(ble_central.devices.values(), key=operator.attrgetter('age'))
        self.adapter.data = []
        self.adapter.data = list(devices)


if __name__ == '__main__':
    BleTestApp().run()
