'''
Android Sysinfo
-----------
'''

from jnius import autoclass
from plyer.facades import Sysinfo
from plyer.platforms.android import activity
from android import api_version, version_codes
Build = autoclass('android.os.Build')
BuildVersion = autoclass('android.os.Build$VERSION')
BuildVersionCodes = autoclass('android.os.Build$VERSION_CODES')
Settings = autoclass('android.provider.Settings')
Intent = autoclass('android.content.Intent')
uri = autoclass('android.net.Uri')
System = autoclass('java.lang.System')


class AndroidSysinfo(Sysinfo):

    def _model_info(self):
        return Build.MODEL

    def _system_info(self):
        return BuildVersion.BASE_OS

    def _platform_info(self):
        return Build.DEVICE

    def _processor_info(self):
        return Build.CPU_ABI

    def _version_info(self):
        sdkint = BuildVersion.SDK_INT
        for name, value in dir(BuildVersionCodes):
            if sdkint == value:
                return ('Android', sdkint, name)
        return ('Android', sdkint, 'UNKNOWN')

    def _architecture_info(self):
        return (Build.CPU_ABI, Build.CPU_ABI2)

    def _device_name(self):
        return Build.MODEL

    def _manufacturer_name(self):
        return Build.MANUFACTURER

    def _kernel_version(self):
        return System.getProperty("os.version")

    def _storage_info(self):
        return ""

    def _screen_dimension(self):
        return ""


def instance():
    return AndroidSysinfo()
