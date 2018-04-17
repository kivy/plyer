'''
	Note::
		This facade depends on:
		- nmcli (Network Manager command line tool)
			It is found in most of the popular distros. Support for other
			managers is not provided yet.
			Source from: https://cgit.freedesktop.org/NetworkManager/NetworkManager/tree/examples/python/gi/show-wifi-networks.py
'''
#from __future__ import print_function
from plyer.facades import Wifi
from subprocess import Popen, PIPE, call, STDOUT
import gi
gi.require_version('NM', '1.0')
from gi.repository import NM

nmc = NM.Client.new()
devs = nmc.get_devices()
def ssid_to_utf8(ap):
	ssid = ap.get_ssid()
	if not ssid:
		return ""
	return NM.utils_ssid_to_utf8(ap.get_ssid().get_data())
def mode_to_string(mode):
	if mode == getattr(NM, '80211Mode').INFRA:
		return "INFRA"
	if mode == getattr(NM, '80211Mode').ADHOC:
		return "ADHOC"
	if mode == getattr(NM, '80211Mode').AP:
		return "AP"
	return "UNKNOWN"
def flags_to_string(flags):
	if flags & getattr(NM, '80211ApFlags').PRIVACY:
		return "PRIVACY"
	return "NONE"
def security_flags_to_string(flags):
	NM_AP_FLAGS = getattr(NM, '80211ApSecurityFlags')
	str = ""
	if flags & NM_AP_FLAGS.PAIR_WEP40:
		str = str + " PAIR_WEP40"
	if flags & NM_AP_FLAGS.PAIR_WEP104:
		str = str + " PAIR_WEP104"
	if flags & NM_AP_FLAGS.PAIR_TKIP:
		str = str + " PAIR_TKIP"
	if flags & NM_AP_FLAGS.PAIR_CCMP:
		str = str + " PAIR_CCMP"
	if flags & NM_AP_FLAGS.GROUP_WEP40:
		str = str + " GROUP_WEP40"
	if flags & NM_AP_FLAGS.GROUP_WEP104:
		str = str + " GROUP_WEP104"
	if flags & NM_AP_FLAGS.GROUP_TKIP:
		str = str + " GROUP_TKIP"
	if flags & NM_AP_FLAGS.GROUP_CCMP:
		str = str + " GROUP_CCMP"
	if flags & NM_AP_FLAGS.KEY_MGMT_PSK:
		str = str + " KEY_MGMT_PSK"
	if flags & NM_AP_FLAGS.KEY_MGMT_802_1X:
		str = str + " KEY_MGMT_802_1X"
	if str:
		return str.lstrip()
	else:
		return "NONE"

def flags_to_security(flags, wpa_flags, rsn_flags):
	str = ""
	if ((flags & getattr(NM, '80211ApFlags').PRIVACY) and
		(wpa_flags == 0) and (rsn_flags == 0)):
		str = str  + " WEP"
	if wpa_flags != 0:
		str = str + " WPA1"
	if rsn_flags != 0:
		str = str + " WPA2"
	if ((wpa_flags & getattr(NM, '80211ApSecurityFlags').KEY_MGMT_802_1X) or
		(rsn_flags & getattr(NM, '80211ApSecurityFlags').KEY_MGMT_802_1X)):
		str = str + " 802.1X"
	return str.lstrip()

class LinuxWifi(Wifi):
	names = {}
	def enable(self):
		return call(['nmcli', 'r', 'wifi', 'on'])

	def disable(self):
		return call(['nmcli', 'r', 'wifi', 'off'])

	def keys(self):
		return ('None' if len(self.names) is 0 else self.names)

	def _is_enabled(self):
		'''
		Returns `True` if wifi is enabled else `False`.
		'''
		enbl = Popen(["nmcli", "radio", "wifi"], stdout=PIPE, stderr=PIPE)
		if enbl.communicate()[0].split()[0].decode("utf-8") == "enabled":
			return True
		else:
			self.enable()
			return True
		return False
	def _start_scanning(self):
		i = 0
		hosts = {}
		for dev in devs:
			if dev.get_device_type() == NM.DeviceType.WIFI:
				for ap in dev.get_access_points():
					data = {}
					strength = ap.get_strength()
					frequency = ap.get_frequency()
					flags = ap.get_flags()
					wpa_flags = ap.get_wpa_flags()
					rsn_flags = ap.get_rsn_flags()
					data['ssid'] = ssid_to_utf8(ap)
					data['bssid'] = ap.get_bssid()
					data['frequency'] = str(frequency)
					data['channel'] = str(NM.utils_wifi_freq_to_channel(frequency))
					data['mode'] = mode_to_string(ap.get_mode())
					data['flags'] = flags_to_string(flags)
					data['wpa_flags'] = security_flags_to_string(wpa_flags)
					data['rsn_flags'] = security_flags_to_string(rsn_flags)
					data['security'] = flags_to_security(flags, wpa_flags, rsn_flags)
					data['strength'] = str(strength)
					hosts[i] = data
					i += 1
		'''
		Returns all the network information.
		'''
		self.names.clear()
		if self._is_enabled():
			for i in hosts:
				self.names[hosts[i]['ssid']] = hosts[i]
		else:
			raise Exception('Wifi not enabled.')

	def _get_network_info(self, name):
		'''
		Starts scanning for available Wi-Fi networks and returns the available,
		devices.
		'''
		ret_list = {}
		ret_list['ssid'] = self.names[name]['ssid']
		ret_list['signal'] = self.names[name]['strength']
		ret_list['frequency'] = self.names[name]['frequency']
		ret_list['encrypted'] = self.names[name]['security']
		ret_list['channel'] = self.names[name]['channel']
		ret_list['address'] = self.names[name]['bssid']
		ret_list['mode'] = self.names[name]['mode']
		if not ret_list['encrypted']:
			return ret_list
		else:
			ret_list['encryption_type'] = self.names[name]['security']
			return ret_list

	def _get_available_wifi(self):
		'''
		Returns the name of available networks.
		'''
		return ('None' if len(self.names) is 0 else self.names)

	def _connect(self, network, parameters):
		'''
		Expects 2 parameters:
			- name/ssid of the network.
			- parameters:
				- password: dict type
		'''
		try:
			self.enable()
		finally:
			password = parameters['password']
			cell = self.names[network]
			call(['nmcli', 'device', 'wifi', 'connect', network, 'password', password])
			return 'And we are connected'

	def _disconnect(self):
		'''
		Disconnect all the networks managed by Network manager.
		'''
		return self.disable()


def instance():
	import sys
	try:
		return LinuxWifi()
	except ImportError:
		sys.stderr.write("We are having problems with the import of libraries..")
	return Wifi()