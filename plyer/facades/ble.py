from uuid import UUID
from time import time


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


class BleDevice(object):
	def __init__(self, announcement, power):
		self.announcement = announcement
		self.company = company = mkintle(announcement[0:2])
		self.company_hex = hexstr(announcement[0:2])
		self.data = data = announcement[2:]
		self.data_hex = hexstr(data)
		self.type = None
		self.prefix = None
		self.uuid = None
		self.major = None
		self.minor = None
		self.tx_power = None
		self.rx_power = power
		self.received = time()

		if len(data) >= 22:
			self.prefix = data[:2]
			self.prefix_hex = hexstr(data[:2])
			self.uuid = UUID(hexstr(data[2:18]))
			self.major = mkint(data[18:20])
			self.minor = mkint(data[20:22])
			self.tx_power = data[22]

			if company == 0x4c and data[0] == 0x02 and data[1] == 0x15:
				self.type = 'iBeacon'
			elif data[0] == 0xbe and data[1] == 0xac:
				self.type = 'AltBeacon'

	@property
	def distance(self):
		if self.tx_power is None:
			return None

		ratio = self.rx_power * (1. / self.tx_power)
		if ratio < 1.0:
			return pow(ratio, 10)
		return 0.89976 * pow(ratio, 7.7095) + 0.111

	@property
	def age(self):
		return time() - self.received

	def __str__(self):
		dist = self.distance
		if dist is not None:
			txrx = 'd={}'.format(dist)
		else:
			txrx = 'rx={}'.format(self.rx_power)
		if self.type:
			return '<BleBeacon type={} uuid={} v={}:{} {}>'.format(
				self.type, self.uuid, self.major, self.minor, txrx)
		if self.uuid:
			return '<BleBeacon company={} prefix={} uuid={} v={}:{} {}>'.format(
				self.company_hex, self.prefix_hex, self.uuid, self.major, self.minor, txrx)
		return '<BleDevice company={} data={} {}>'.format(self.company_hex, self.data_hex, txrx)


class Ble(object):
	'''Bluetooth low energy facade.
	'''

	Device = BleDevice

	on_state = None
	on_discover = None

	def init(self):
		'''Initialize BLE framework.'''
		raise NotImplementedError()

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

	def start_scanning(self):
		'''Scan for BLE advertisements.
		'''
		return self._start_scanning()

	def stop_scanning(self):
		'''Stop scanning for BLE advertisements.
		'''
		return self._stop_scanning()

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

	def _start_scanning(self):
		raise NotImplementedError()

	def _stop_scanning(self):
		raise NotImplementedError()

