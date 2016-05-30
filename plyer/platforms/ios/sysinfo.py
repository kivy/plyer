'''
ios Sysinfo
-----------
'''

from plyer.facades import Sysinfo
from pyobjus import autoclass
from pyobjus.dylib_manager import load_dylib, make_dylib
import sys
load_framework('/System/Library/Frameworks/UIKit.framework')
make_dylib('plyer/platforms/ios/libs/sysinfo.m', frameworks=['Foundation'],
           out='sysinfo.dylib')
load_dylib('sysinfo.dylib')
UIDevice = autoclass('UIDevice')
UIScreen = autoclass('UIScreen')
NSProcessInfo = autoclass('NSProcessInfo')


class AndroidSysinfo(Sysinfo):

    def __init__(self, **kwargs):
        super(AndroidSysinfo, self).__init__(**kwargs)
        self.device = UIDevice.currentDevice()

    def _model_info(self):
        return self.device.model

    def _system_info(self):
        return self.device.systemName

    def _platform_info(self):
        return sys.platform

    def _processor_info(self):
        return " "

    def _version_info(self):
        return (self.device.systemVersion, " ", " ")

    def _architecture_info(self):
        sizeClass = autoclass('SizeClass')
        instance = sizeClass.alloc().init()
        bit = instance.get_bit_size()
        return ("{}".format(bit), " ")

    def _device_name(self):
        return self.device.name

    def _manufacturer_name(self):
        return "Apple Inc."

    def _kernel_version(self):
        processinfo = NSProcessInfo()
        return processinfo.operatingSystemVersionString

    def _storage_info(self):
        Storage = autoclass('StorageClass')
        instance = Storage.alloc().init()
        return str(instance.get_total_space())

    def _screen_dimension(self):
        screen = UIScreen.mainScreen().bounds
        width = screen.size.width
        height = screen.size.height
        return (height, width)


def instance():
    return AndroidSysinfo()
