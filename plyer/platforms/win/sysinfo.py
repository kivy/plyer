import platform
import os
import re
import sys
import ctypes
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo
from plyer.platforms.win.libs import win_api_defs


class WindowsSysinfo(Sysinfo):

    def _call_wmic(self, subcmd):
        cmd = ['wmic', ] + subcmd
        print(cmd)
        p = Popen(cmd, stderr=PIPE, stdout=PIPE)
        data = p.communicate()[0]
        splits = data.strip().splitlines()
        clean_list = []
        for split in splits:
            i = split.strip()
            if i != '' and i.lower() != subcmd[-1].lower():
                clean_list.append(i)
        return clean_list

    def _model_info(self):
        '''
        Returns Model information for example: "HP 2000 Notebook PC"
        '''
        model = self._call_wmic(['computersystem', 'get', 'model'])[0]
        if model.lower() == 'system product name':
            model = self._call_wmic(['baseboard', 'get', 'product'])[0]
            name = self._call_wmic(['computersystem', 'get', 'caption'])[0]
            model = "{0} ({1})".format(name, model)

        return model

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
        l = []
        l.append(self._call_wmic(['cpu', 'get', 'name'])[0])
        cores = int(self._call_wmic(['cpu', 'get', 'numberofcores'])[0])
        if cores == 1:
            l.append("1 core")
        else:
            l.append("{0} cores".format(cores))
        l.append(self._call_wmic(['cpu', 'get', 'manufacturer'])[0])
        # return platform.processor()
        info = re.sub("(?:\t+|[ ]{2,})", ' ', ", ".join(l))
        return info

    def _version_info(self):
        '''
        Returns the version of OS in a tuple for example:
        "8 6.2.9200 "
        '''
        try:
            v = self._call_wmic(['os', 'get', 'caption'])[0]
            return v  # WARNING use tuple
        except:
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
        name = self._call_wmic(['computersystem', 'get', 'manufacturer'])[0]
        if name.lower() == 'system manufacturer':
            name = self._call_wmic(['baseboard', 'get', 'manufacturer'])[0]
        return name

    def _kernel_version(self):
        '''
        Returns the kernel version, for example: "8"
        '''
        return platform.uname()[2]

    def _storage_info(self, path='c:'):
        '''
        Returns the amount of storage (RAM) in GB for example: "3.9 GB"
        '''
        drive = path.split(':')[0] + ":"
        cmd = ['fsutil', 'volume', 'diskfree', drive]
        p = Popen(cmd, stderr=PIPE, stdout=PIPE)
        data = p.communicate()[0]
        splits = data.strip().splitlines()
        free_bytes = splits[2].split(':')[-1].strip()
        return int(free_bytes)

    def _memory_info(self):
        return int(self._call_wmic(['computersystem', 'get',
                                    'TotalPhysicalMemory'])[0])

    def _screen_resolution(self):
        '''
        Returns the screen resolution for example: "[1366, 768]"
        '''
        return (win_api_defs.GetSystemMetrics(0),
                win_api_defs.GetSystemMetrics(1))


def instance():
    return WindowsSysinfo()
