import platform
import os
import re
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo
from plyer.platforms.win.libs import win_api_defs


class WindowsSysinfo(Sysinfo):

    values = {}

    def _ensure_sysinfo(self):
        '''
        Helping private method for extracting system information.
        '''

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
        '''
        Returns Model information for example: "HP 2000 Notebook PC"
        '''
        if 'System Model' in self.values:
            return self.values['System Model']
        return self._ensure_sysinfo()['System Model']

    def _system_name(self):
        '''
        Returns System's OS name for example: "Windows"
        '''
        return platform.system()

    def _platform_info(self):
        '''
        Returns the platform's name for example: "Windows-8-6.2.9200"
        '''
        return platform.platform()

    def _processor_info(self):
        '''
        Returns the type of processor for example:
        "Intel64 Family 6 Model 42 Stepping 7, GenuineIntel"
        '''
        return platform.processor()

    def _version_info(self):
        '''
        Returns the version of OS in a tuple for example:
        "8 6.2.9200 "
        '''
        return platform.win32_ver()

    def _architecture_info(self):
        '''
        Returns the architecture in a tuple, for example:
        "('32bit', "WindowsPE")""
        '''
        return platform.architecture()

    def _device_name(self):
        '''
        Returns the device's name, for example: "DESKTOP-8UFTHDN"
        '''
        return platform.uname()[1]

    def _manufacturer_name(self, **kwargs):
        '''
        Returns manufacturer's name, for example: "Hewlett-Packard"
        '''
        if 'System Manufacturer' in self.values:
            return self.values['System Manufacturer']
        return self._ensure_sysinfo()['System Manufacturer']

    def _kernel_version(self):
        '''
        Returns the kernel version, for example: "8"
        '''
        return platform.uname()[2]

    def _storage_info(self):
        '''
        Returns the amount of storage (RAM) in GB for example: "3.9 GB"

        Note: The returned output from `os.popen2("SYSTEMINFO")` is string,
        with `,`(commas) between integer values(in MB) but the output should
        be same for each platform, hence in GB.
        '''
        try:
            if 'Total Physical Memory' in self.values:
                storage = self.values['Total Physical Memory']
            else:
                storage = self._ensure_sysinfo()['Total Physical Memory']
            memory, unit = storage.split(' ')
            try:
                temp = ''
                for i in memory.split(','):
                    temp = temp + i
                memory = temp
            except:
                pass
            if (unit.lower() == "kb"):
                return str(round(int(memory) / (1024.0 * 1024.0), 2)) + " GB"
            elif (unit.lower() == "mb"):
                return str(round(int(memory) / 1024.0, 2)) + " GB"
            elif (unit.lower() == "gb"):
                return str(int(memory)) + " GB"
        except:
            return self._ensure_sysinfo()['Total Physical Memory']

    def _screen_resolution(self):
        '''
        Returns the screen resolution for example: "[1366, 768]"
        '''
        return (win_api_defs.GetSystemMetrics(0),
                win_api_defs.GetSystemMetrics(1))


def instance():
    return WindowsSysinfo()
