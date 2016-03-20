
class BlePeripheralCharacteristic(object):
    property = type('BlePeripheralCharacteristic.property', (object,), {
        'broadcast': 0x01,
        'read': 0x02,
        'write_without_response': 0x04,
        'write': 0x08,
        'notify': 0x10,
        'indicate': 0x20,
        'authenticated_signed_writes': 0x40,
        'extended_properties': 0x80,
        'notify_encryption_required': 0x100,
        'indicate_encryption_required': 0x200
    })

    permission = type('BlePeripheralCharacteristic.permission', (object,), {
        'readable': 0x01,
        'writeable': 0x02,
        'read_encryption_required': 0x04,
        'write_encryption_required': 0x08,
    })

    def __init__(self, uuid, value=None, permissions=None, properties=None):
        self.uuid = uuid
        self.value = value
        self.permissions = permissions
        self.properties = properties
        self.on_read = None
        self.on_write = None
        self.on_subscribe = None
        self.init()

    def set_callbacks(self, on_read=None, on_write=None, on_subscribe=None):
        if on_read:
            self.on_read = on_read
        if on_write:
            self.on_write = on_write
        if on_subscribe:
            self.on_subscribe = on_subscribe

    def init(self):
        raise NotImplementedError()

    def set_value(self, value):
        raise NotImplementedError()


class BlePeripheralService(object):
    def __init__(self, uuid, primary=True):
        self.uuid = uuid
        self.primary = primary
        self.init()

    def init(self):
        raise NotImplementedError()

    def add_characteristic(self, characteristic):
        raise NotImplementedError()


class BlePeripheral(object):
    '''Bluetooth low energy peripheral facade.
    '''

    Characteristic = BlePeripheralCharacteristic
    Service = BlePeripheralService

    on_state = None
    on_service_added = None
    on_service_error = None
    on_advertising_started = None
    on_advertising_error = None
    on_characteristic_subscribed = None
    on_characteristic_write = None

    def init(self):
        '''Initialize BLE framework.'''
        raise NotImplementedError()

    @property
    def state(self):
        '''Get current BLE peripheral state.'''
        return self._state()

    @property
    def has_ble(self):
        '''Check if device supports BLE peripheral.'''
        return self._has_ble()

    @property
    def is_advertising(self):
        return self._is_advertising()

    def set_callbacks(self, on_state=None, on_service_added=None,
                      on_service_error=None, on_advertising_started=None,
                      on_advertising_error=None,
                      on_characteristic_subscribed=None,
                      on_characteristic_write=None):
        '''Set callback functions.
        '''
        if on_state:
            self.on_state = on_state
        if on_service_added:
            self.on_service_added = on_service_added
        if on_service_error:
            self.on_service_error = on_service_error
        if on_advertising_started:
            self.on_advertising_started = on_advertising_started
        if on_advertising_error:
            self.on_advertising_error = on_advertising_error
        if on_characteristic_subscribed:
            self.on_characteristic_subscribed = on_characteristic_subscribed
        if on_characteristic_write:
            self.on_characteristic_write = on_characteristic_write

    def add_service(self, service):
        assert isinstance(service, BlePeripheralService)
        self._add_service(service)

    def start_advertising(self, name=None):
        if not name:
            name = 'plyer-ble'
        self._start_advertising(name)

    def stop_advertising(self):
        self._stop_advertising()

    # private

    def _state(self):
        raise NotImplementedError()

    def _has_ble(self):
        raise NotImplementedError()

    def _is_advertising(self):
        raise NotImplementedError()

    def _add_service(self, service):
        raise NotImplementedError()

    def _start_advertising(self, name):
        raise NotImplementedError()

    def _stop_advertising(self):
        raise NotImplementedError()

