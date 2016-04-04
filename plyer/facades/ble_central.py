from uuid import UUID
from time import time

try:
    from six import with_metaclass
except ImportError:
    def with_metaclass(meta, *bases):
        """Create a base class with a metaclass."""
        # This requires a bit of explanation: the basic idea is to make a dummy
        # metaclass for one level of class instantiation that replaces itself with
        # the actual metaclass.
        class metaclass(meta):

            def __new__(cls, name, this_bases, d):
                return meta(name, bases, d)
        return type.__new__(metaclass, 'temporary_class', (), {})


def twos(n):
    n &= 0xff
    if (n & 0x80) != 0:
        n -= 256
    return n


def hexstr(il):
    return ''.join(['{:02x}'.format(i) for i in il])


def mkint(il):
    if not il:
        return 0
    ii = il[0]
    for i in il[1:]:
        ii = (ii << 8) + i
    return ii


def mkintle(il):
    return mkint(list(reversed(il)))


class BleDeviceMeta(type):
    def __call__(cls, *args, **kwargs):
        device = super(BleDeviceMeta, cls).__call__(*args, **kwargs)
        uuid = device.uuid
        if uuid:
            key = device.key
            existing = BleDevice.devices.get(key)
            if existing:
                existing._update(device)
                device = existing
            BleDevice.devices[device.key] = device
        cls.prune_devices()
        return device

    last_prune = 0

    def prune_devices(cls):
        t = time()
        if cls.last_prune < (t - 1):
            # in case of a lot of beacons, we don't want to be iterating and
            # pruning a long list many times per second, so we'll limit it to
            # once per second
            cls.last_prune = t
            max_age = BleDevice.max_age
            devices = BleDevice.devices
            for key in list(devices.keys()):
                if devices[key].age > max_age:
                    del devices[key]


class BleDevice(with_metaclass(BleDeviceMeta)):
    devices = {}
    max_age = 60

    @classmethod
    def clear_devices(cls):
        BleDevice.devices = {}

    uuid = None
    name = None
    rx_power = None
    received = None
    update = None
    announcement = None
    company = None
    company_hex = None
    data = None
    data_hex = None
    type = None
    prefix = None
    beacon_uuid = None
    major = None
    minor = None
    tx_power = None
    prefix_hex = None
    services = None

    @property
    def key(self):
        return self.uuid, self.beacon_uuid

    def __init__(self, uuid, name, power, announcement=None, services=None):
        self.uuid = UUID(uuid)
        self.name = name
        self.rx_power = power
        self.received = self.updated = time()

        if announcement:
            self.announcement = announcement
            self.company = company = mkintle(announcement[0:2])
            self.company_hex = hexstr(announcement[0:2])
            self.data = data = announcement[2:]
            self.data_hex = hexstr(data)

            if len(data) >= 22:
                self.prefix = data[:2]
                self.prefix_hex = hexstr(data[:2])
                self.beacon_uuid = UUID(hexstr(data[2:18]))
                self.major = mkintle(data[18:20])
                self.minor = mkintle(data[20:22])
                tx = twos(data[22])
                self.tx_power = float(tx)

                if company == 0x4c and data[0] == 0x02 and data[1] == 0x15:
                    self.type = 'iBeacon'
                elif data[0] == 0xbe and data[1] == 0xac:
                    self.type = 'AltBeacon'

        if services:
            self.services = {UUID(s): None for s in services}

    def _update(self, new):
        self.rx_power = new.rx_power
        self.updated = new.updated

        if self.beacon_uuid:
            self.data = new.data
            self.data_hex = new.data_hex
            self.tx_power = new.tx_power

    @property
    def distance(self):
        try:
            ratio = self.rx_power / self.tx_power
            if ratio < 1.0:
                return pow(ratio, 10)
            return 0.89976 * pow(ratio, 7.7095) + 0.111
        except Exception:
            return -1

    @property
    def age(self):
        return time() - self.received

    @property
    def seen(self):
        return time() - self.updated

    def __str__(self):
        preamble = 'uuid={} name={}'.format(self.uuid, self.name)
        dist = self.distance
        txrx = 'rx={}'.format(self.rx_power)
        tx = self.tx_power
        if tx is not None:
            txrx = 'tx={} {}'.format(tx, txrx)
        if dist >= 0:
            txrx = 'd={} {}'.format(dist, txrx)
        name = 'BleBeacon' if self.beacon_uuid else 'BleDevice'
        devinfo = ''
        if self.beacon_uuid:
            if self.type:
                devinfo += ' type={} beacon={} v={}:{}'.format(
                    self.type, self.beacon_uuid, self.major, self.minor)
            else:
                devinfo += ' company={} prefix={} beacon={} v={}:{}'.format(
                    self.company_hex, self.prefix_hex, self.beacon_uuid,
                    self.major, self.minor)
        if self.services:
            devinfo += ' services={}'.format(len(self.services.keys()))
        return '<{} {}{} {}>'.format(name, preamble, devinfo, txrx)

    def connect(self, on_connect=None, on_disconnect=None):
        self._connect(on_connect, on_disconnect)

    def _connect(self, on_connect=None, on_disconnect=None):
        raise NotImplementedError()

    def disconnect(self, callback=None):
        self._disconnect(callback)

    def _disconnect(self, callback=None):
        raise NotImplementedError()


class BleCentral(object):
    '''Bluetooth low energy central facade.
    '''

    Device = BleDevice

    on_state = None
    on_discover = None

    def init(self):
        '''Initialize BLE framework.'''
        raise NotImplementedError()

    @property
    def devices(self):
        return self.Device.devices

    @property
    def state(self):
        '''Get current Bluetooth state.'''
        return self._state()

    @property
    def is_scanning(self):
        return self._is_scanning()

    @property
    def has_ble(self):
        '''Check if device supports BLE.
        '''
        return self._has_ble()

    def start_scanning(self, allow_duplicates=True):
        '''Scan for BLE advertisements.
        '''
        return self._start_scanning(allow_duplicates)

    def stop_scanning(self):
        '''Stop scanning for BLE advertisements.
        '''
        try:
            return self._stop_scanning()
        finally:
            self.Device.clear_devices()

    def set_callbacks(self, on_state=None, on_discover=None):
        '''Set callback functions.
        '''
        if on_state:
            self.on_state = on_state
        if on_discover:
            self.on_discover = on_discover

    # private

    def _state(self):
        raise NotImplementedError()

    def _is_scanning(self):
        raise NotImplementedError()

    def _has_ble(self):
        raise NotImplementedError()

    def _start_scanning(self, allow_duplicates=True):
        raise NotImplementedError()

    def _stop_scanning(self):
        raise NotImplementedError()

