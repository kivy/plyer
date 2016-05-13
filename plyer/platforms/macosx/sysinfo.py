import platform
from plyer.facades import Sysinfo


class OSXSysinfo(Sysinfo):

    def _model_info(self):
        return ""

    def _system_info(self):
        return platform.system()

    def _platform_info(self):
        return platform.platform()

    def _processor_info(self):
        return platform.processor()

    def _version_info(self):
        return platform.mac_ver()

    def _architecture_info(self):
        return platform.architecture()

    def _device_name(self):
        return platform.uname()[1]

    def _manufacturer_name(self):
        return ""

    def _kernel_version(self):
        return platform.uname()[2]

    def _storage_info(self):
        return ""

    def _screen_dimension(self):
        return ""


def instance():
    return OSXSysinfo()
