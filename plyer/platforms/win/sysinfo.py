import platform
import os
import re
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo
from plyer.platforms.win.libs import screenmetric


class WindowsSysinfo(Sysinfo):

    values = {}

    def __init__(self, **kwargs):
        self.SysInfo()

    def SysInfo(self):

        cache = os.popen2("SYSTEMINFO")
        source = cache[1].read()
        sysOpts = ["System Manufacturer", "System Model",
                   "Total Physical Memory"]

        for opt in sysOpts:
            self.values[opt] = [item.strip() for item in
                                re.findall("%s:\w*(.*?)\n" % (opt),
                                source, re.IGNORECASE)][0]

    def _model_info(self, **kwargs):
        return self.values['System Model']

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

    def _manufacturer_name(self, **kwargs):
        return self.values['System Manufacturer']

    def _kernel_version(self):
        return platform.uname()[2]

    def _storage_info(self):
        return self.values['Total Physical Memory']

    def _screen_dimension(self):
        return (screenmetric.get_SystemMetrics(0),
                screenmetric.get_SystemMetrics(1))


def instance():
    return WindowsSysinfo()
