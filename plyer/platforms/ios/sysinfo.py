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


class IosSysinfo(Sysinfo):

    def __init__(self, **kwargs):
        super(IosSysinfo, self).__init__(**kwargs)
        self.device = UIDevice.currentDevice()

    def _model_info(self):
        '''
        Returns the model info for example:
        '''
        return self.device.model

    def _system_name(self):
        '''
        Returns the system's OS name for example:
        '''
        return self.device.systemName

    def _platform_info(self):
        '''
        Returns platform's name for example:
        '''
        return sys.platform

    def _processor_info(self):
        '''
        Returns the type of processor for example:
        '''
        return " "

    def _version_info(self):
        '''
        Returns the version of OS in a tuple for example:
        '''
        return (self.device.systemVersion, " ", " ")

    def _architecture_info(self):
        '''
        Returns the architecture in a tuple for example:
        '''
        sizeClass = autoclass('SizeClass')
        instance = sizeClass.alloc().init()
        bit = instance.get_bit_size()
        return ("{}".format(bit), " ")

    def _device_name(self):
        '''
        Returns the device name for example:
        '''
        return self.device.name

    def _manufacturer_name(self):
        '''
        Returns the manufacturer's name for example:
        '''
        return "Apple Inc."

    def _kernel_version(self):
        '''
        Returns the kernel version for example:
        '''
        processinfo = NSProcessInfo()
        return processinfo.operatingSystemVersionString

    def _storage_info(self):
        '''
        Returns the amount of storage (RAM) in GB. for example:
        '''
        Storage = autoclass('StorageClass')
        instance = Storage.alloc().init()
        return str(instance.get_total_space())

    def _screen_resolution(self):
        '''
        Returns the screen resolution for example:
        '''
        screen = UIScreen.mainScreen().bounds
        width = screen.size.width
        height = screen.size.height
        return (height, width)


def instance():
    return IosSysinfo()
