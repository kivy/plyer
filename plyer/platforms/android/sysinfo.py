'''
Android Sysinfo
-----------
'''

from jnius import autoclass
from plyer.facades import Sysinfo
from plyer.platforms.android import activity
import platform
Build = autoclass('android.os.Build')
Settings = autoclass('android.provider.Settings')
Intent = autoclass('android.content.Intent')
uri = autoclass('android.net.Uri')


class AndroidSysinfo(Call):

    def _system_info(self):
        return platform.system()

    def _platform_info(self):
        return platform.platform()

    def _processor_info(self):
        return platform.processor()

    def _version_info(self):
        return Build.VERSION.INCREMENTAL

def instance():
    return AndroidSysinfo()