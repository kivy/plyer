import platform
from plyer.facades import Sysinfo


class LinuxSysinfo(Sysinfo):

    def _system_info(self):
        return platform.system()

    def _platform_info(self):
        return platform.platform()

    def _processor_info(self):
        return platform.processor()

    def _dist_info(self):
        if platform.system() == "Linux": 
            return platform.dist()
        else:
            raise NotImplementedError()


def instance():
    return LinuxSysinfo()