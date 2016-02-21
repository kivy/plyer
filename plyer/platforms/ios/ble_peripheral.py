'''
iOS BLE Peripheral
------------------

'''
from plyer.platforms.macosx.ble_peripheral import OSXBlePeripheral


class iOSBlePeripheral(OSXBlePeripheral):
	pass


def instance():
	return iOSBlePeripheral()

