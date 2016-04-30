import platform
from plyer.facades import Sysinfo


class LinuxSysinfo(Sysinfo):

    def _system_info(self):
        return platform.system()

    def _platform_info(self):
        return platform.platform()

    def _processor_info(self):
        return platform.processor()

    def _version_info(self):
        # includes Distro_name, version and name
        return platform.dist()


def instance():
    return LinuxSysinfo()