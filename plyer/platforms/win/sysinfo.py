import platform
from plyer.facades import Sysinfo


class WindowsSysinfo(Sysinfo):

    def _system_info(self):
        return platform.system()

    def _platform_info(self):
        return platform.platform()

    def _processor_info(self):
        return platform.processor()

    def _dist_info(self):
        if platform.system() == "Windows": 
            return platform.win32_ver()
        else:
            raise NotImplementedError()


def instance():
    return WindowsSysinfo()