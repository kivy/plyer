import platform
from plyer.facades import Sysinfo


class WindowsSysinfo(Sysinfo):

    def _system_info(self):
        return platform.system()

    def _platform_info(self):
        return platform.platform()

    def _processor_info(self):
        return platform.processor()

    def _version_info(self):
        return platform.win32_ver()

    def _architecture_info(self):
        return platform.architecture()

    def _device_name(self):
        return platform.uname()[1]

    def _manufacturer_name(self):
        pass


def instance():
    return WindowsSysinfo()
