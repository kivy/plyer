'''
iOS BLE Central
---------------

'''
from plyer.platforms.macosx.ble_central import OSXBleCentral


class iOSBleCentral(OSXBleCentral):
	pass


def instance():
	return iOSBleCentral()

