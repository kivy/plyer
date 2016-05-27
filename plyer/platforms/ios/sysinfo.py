'''
ios Sysinfo
-----------
'''

from plyer.facades import Sysinfo
from pyobjus import autoclass
load_framework('/System/Library/Frameworks/UIKit.framework')
UIDevice = autoclass('UIDevice')
UIScreen = autoclass('UIScreen')


class AndroidSysinfo(Sysinfo):

    def __init__(self, **kwargs):
        super(AndroidSysinfo, self).__init__(**kwargs)
        self.device = UIDevice.currentDevice()

    def _model_info(self):
        return self.device.model

    def _system_info(self):
        return self.device.systemName

    def _platform_info(self):
        return " "

    def _processor_info(self):
        return " "

    def _version_info(self):
        return (self.device.systemVersion," "," ")

    def _architecture_info(self):
        return (" ", " ")

    def _device_name(self):
        return self.device.name

    def _manufacturer_name(self):
        return "Apple Inc."

    def _kernel_version(self):
        return " "

    def _storage_info(self):
        return " "

    def _screen_dimension(self):
        screen = UIScreen.mainScreen().bounds
        width = screen.size.width
        height = screen.size.height
        return (height, width)


def instance():
    return AndroidSysinfo()
