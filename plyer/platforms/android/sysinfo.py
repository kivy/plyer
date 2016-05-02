'''
Android Sysinfo
-----------
'''

from jnius import autoclass
from plyer.facades import Sysinfo
from plyer.platforms.android import activity
Build = autoclass('android.os.Build')
Settings = autoclass('android.provider.Settings')
Intent = autoclass('android.content.Intent')
uri = autoclass('android.net.Uri')
System = autoclass('java.lang.System')


class AndroidSysinfo(Sysinfo):

    def _system_info(self):
        return Build.DISPLAY

    def _platform_info(self):
        return Build.DEVICE

    def _processor_info(self):
        return Build.CPU_ABI

    def _version_info(self):
        return Build.FINGERPRINT

    def _architecture_info(self):
        return (Build.CPU_ABI, Build.CPU_ABI2)

    def _device_name(self):
        return Build.MODEL

    def _manufacturer_name(self):
        return Build.MANUFACTURER


def instance():
    return AndroidSysinfo()
