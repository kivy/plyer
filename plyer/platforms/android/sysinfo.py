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

    def _model_info(self, **kwargs):
        return ""

    def _system_info(self):
        return BuildVersion.BASE_OS

    def _platform_info(self):
        return Build.DEVICE

    def _processor_info(self):
        return Build.CPU_ABI

    def _version_info(self):
        version = str(BuildVersion.RELEASE)
        if version >= 1.0 and version < 1.1:
            return ("Android", version, "BASE")
        elif version == 1.1:
            return ("Android", version, "BASE_1_1")
        elif version == 1.5:
            return ("Android", version, "CUPCAKE")
        elif version == 1.6:
            return ("Android", version, "DONUT")
        elif version >= 2.0 and version < 2.0.1:
            return ("Android", version, "ECLAIR")
        elif version >= 2.0.1 and version < 2.1:
            return ("Android", version, "ECLAIR_0_1")
        elif version == 2.1:
            return ("Android", version, "ECLAIR_MR1")
        elif version >= 2.2 and version <= 2.2.3:
            return ("Android", version, "FROYO")
        elif version >= 2.3 and version < 2.3.3:
            return ("Android", version, "GINGERBREAD")
        elif version >= 2.3.3 and version <= 2.3.7:
            return ("Android", version, "GINGERBREAD_MR1")
        elif version >= 3.0 and version < 3.1:
            return ("Android", version, "HONEYCOMB")
        elif version >= 3.1 and version < 3.2:
            return ("Android", version, "HONEYCOMB_MR1")
        elif version >= 3.2 and version <= 3.2.6:
            return ("Android", version, "HONEYCOMB_MR2")
        elif version >= 4.0 and version < 4.0.3:
            return ("Android", version, "ICE_CREAM_SANDWICH")
        elif version >= 4.0.3 and version <= 4.0.4:
            return ("Android", version, "ICE_CREAM_SANDWICH_MR1")
        elif version >= 4.1 and version < 4.2:
            return ("Android", version, "JELLY_BEAN")
        elif version >= 4.2 and version < 4.3:
            return ("Android", version, "JELLY_BEAN_MR1")
        elif version >= 4.3.0 and version <= 4.3.1:
            return ("Android", version, "JELLY_BEAN_MR2")
        elif version >= 4.4 and version < 4.4.1:
            return ("Android", version, "KITKAT")
        elif version >= 4.4.1 and version < 4.4.2:
            return ("Android", version, "KITKAT_MR1")
        elif version >= 4.4.2 and version <= 4.4.4:
            return ("Android", version, "KITKAT_MR2")
        elif version >= 5.0 and version < 5.1:
            return ("Android", version, "LOLLIPOP")
        elif version >= 5.1 and version <= 5.1.1:
            return ("Android", version, "LOLLIPOP_MR1")
        elif version == 6.0:
            return ("Android", version, "MARSHMALLOW")
        else:
            return ("Android", 0.0, "Unknown version")

    def _architecture_info(self):
        return (Build.CPU_ABI, Build.CPU_ABI2)

    def _device_name(self):
        return Build.MODEL

    def _manufacturer_name(self, **kwargs):
        return Build.MANUFACTURER

    def _kernel_version(self):
        return System.getProperty("os.version")

    def _storage_info(self):
        return ""

    def _screen_dimension(self):
        return ""


def instance():
    return AndroidSysinfo()
