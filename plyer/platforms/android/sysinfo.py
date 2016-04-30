'''
Android Sysinfo
-----------
'''

from jnius import autoclass
from plyer.facades import Sysinfo
from plyer.platforms.android import activity
Build = autoclass('android.os.Build')
Settings = autoclass('android.provider.Settings')


class AndroidSysinfo(Call):

    def _system_info(self):
        pass

    def _platform_info(self):
        pass

    def _processor_info(self):
        pass

    def _version_info(self):
        #not tested yet. just from docs.
        return Build.VERSION.INCREMENTAL

def instance():
    return AndroidSysinfo()