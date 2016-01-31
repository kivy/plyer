'''
BLE example
'''
import operator
from kivy.adapters.listadapter import ListAdapter
from kivy.app import App
from kivy.properties import AliasProperty, BooleanProperty, ObjectProperty, StringProperty, NumericProperty, Clock
from kivy.uix.boxlayout import BoxLayout

from plyer import ble


class DeviceItem(BoxLayout):
	uuid = StringProperty('none')
	beacon_type = StringProperty('unknown')
	distance = NumericProperty(0)
	age = NumericProperty(-1)
	total = NumericProperty(-1)


class BleTestApp(App):
	state = StringProperty('unknown')
	scanning = BooleanProperty(False)
	ble_available = BooleanProperty(False)

	adapter = ObjectProperty()

	devices = {}

	def __init__(self, **kwargs):
		super(BleTestApp, self).__init__(**kwargs)
		self.adapter = ListAdapter(data=[], cls=DeviceItem, args_converter=self.device_args_converter)

	@staticmethod
	def device_args_converter(index, obj):
		return {'uuid': str(obj.uuid),
		        'distance': obj.distance,
		        'beacon_type': obj.type,
		        'age': int(obj.age),
		        'total': int(obj.age_total + obj.age)}

	def on_start(self):
		ble.set_callbacks(on_state=self.ble_state, on_discover=self.discover)
		self.scanning = ble.is_scanning
		Clock.schedule_interval(self.update_list, 0.5)

	def toggle_scan(self):
		if ble.has_ble:
			if ble.is_scanning:
				ble.stop_scanning()
				self.scanning = False
			else:
				ble.start_scanning()
				self.scanning = True

	def ble_state(self, state):
		self.state = state
		self.ble_available = ble.has_ble
		self.scanning = ble.is_scanning

	def discover(self, device):
		if device.uuid:
			prev = self.devices.get(device.uuid)
			if prev:
				device.age_total = prev.age_total + prev.age
			else:
				device.age_total = 0
			self.devices[device.uuid] = device

	def update_list(self, *args):
		for key in list(self.devices.keys()):
			if self.devices[key].age >= 60.:
				del self.devices[key]
		devices = sorted(self.devices.values(), key=operator.attrgetter('age'))
		self.adapter.data = []
		self.adapter.data = list(devices)


if __name__ == '__main__':
	BleTestApp().run()
