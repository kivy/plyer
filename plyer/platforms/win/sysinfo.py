import platform
import os
import re
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo
from plyer.platforms.win.libs import win_api_defs


class WindowsSysinfo(Sysinfo):

    values = {}

    def _ensure_sysinfo(self):

        cache = os.popen2("SYSTEMINFO")
        source = cache[1].read()
        sysOpts = ["System Manufacturer", "System Model",
                   "Total Physical Memory"]

        for opt in sysOpts:
            self.values[opt] = [item.strip() for item in
                                re.findall("%s:\w*(.*?)\n" % (opt),
                                source, re.IGNORECASE)][0]
        return self.values

    def _model_info(self):
        if 'System Model' in self.values:
            return self.values['System Model']
        return self._ensure_sysinfo()['System Model']

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
        if 'System Manufacturer' in self.values:
            return self.values['System Manufacturer']
        return self._ensure_sysinfo()['System Manufacturer']

    def _kernel_version(self):
        return platform.uname()[2]

    def _storage_info(self):
        if 'Total Physical Memory' in self.values:
            return self.values['Total Physical Memory']
        return self._ensure_sysinfo()['Total Physical Memory']

    def _screen_dimension(self):
        return (win_api_defs.GetSystemMetrics(0),
                win_api_defs.GetSystemMetrics(1))


def instance():
    return WindowsSysinfo()
