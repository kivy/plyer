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
        # includes release, version and ptype.
        return platform.win32_ver()

def instance():
    return WindowsSysinfo()