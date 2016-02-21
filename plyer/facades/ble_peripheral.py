
class BlePeripheralCharacteristic(object):
    pass


class BlePeripheralService(object):
    def __init__(self, uuid, primary=True):
        self.uuid = uuid
        self.primary = primary
        self.init()

    def init(self):
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
                      on_advertising_error=None):
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

