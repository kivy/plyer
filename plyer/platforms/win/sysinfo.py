import platform
import re
import sys
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo
from plyer.platforms.win.libs import win_api_defs


class WindowsSysinfo(Sysinfo):

    def _call_wmic(self, args, as_list=False):
        """Helper method to read output of Windows wmic utility
        * **args** *(list)*: list of 3 arguments to wmic
        * **as_list** *(boolean)*: returns list of output instead of
            default first element only.
        """
        cmd = ['args', ] + args
        print(cmd)
        p = Popen(cmd, stderr=PIPE, stdout=PIPE)
        data = p.communicate()[0]
        splits = data.strip().splitlines()
        clean_list = []
        for split in splits:
            i = split.strip()
            if i != '' and i.lower() != args[-1].lower():
                clean_list.append(i)

        if as_list:
            return clean_list
        else:
            return clean_list[0]

    def _model_info(self, alias=True):
        """Returns Model information for example: "HP 2000 Notebook PC"
        * if *alias* is True, try replacing default value of
        'System Product Name' with '<PC name> (<Main Board model name>')
        """
        model = self._call_wmic(['computersystem', 'get', 'model'])
        if alias and model.lower() in ('system product name', ''):
            model = self._call_wmic(['baseboard', 'get', 'product'])
            name = self._call_wmic(['computersystem', 'get', 'caption'])
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
        """Returns the information of processor as tuple-like object of
        * **model** *(str)*: CPU model name or ''
        * **manufacturer** *(str)*: manufacturer name
        * **arch** *(str)*: architecture info
        * **cores** *(int)*: number of physical cores or None
        NOTE add example
        """
        model = self._call_wmic(['cpu', 'get', 'name'])
        cores = int(self._call_wmic(['cpu', 'get', 'numberofcores']))
        manf = self._call_wmic(['cpu', 'get', 'manufacturer'])
        # return platform.processor()
        model = re.sub("(?:\t+|[ ]{2,})", ' ', model)
        return self.CpuNamedTuple(model=model, manufacturer=manf,
                                  cores=cores, arch=platform.machine())

    def _version_info(self):
        '''
        Returns the version of OS in a tuple for example:
        ('Microsoft Windows 8.1 Pro', '6.3.9600', '')
        (release, version, csd, ptype)
        '''
        ver_win32 = platform.win32_ver()
        try:
            ver = self._call_wmic(['os', 'get', 'caption'])
        except:
            return ver_win32
        else:
            return (ver, ver_win32[1], ver_win32[2])

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

    def _manufacturer_name(self, alias=True, **kwargs):
        """Returns manufacturer's name, for example: "Hewlett-Packard"
        * if *alias* is True, try replacing default value of
        'System Manufacturer' with Main Board vendor
        """
        name = self._call_wmic(['computersystem', 'get', 'manufacturer'])
        if alias and name.lower() in ('system manufacturer', ''):
            name = self._call_wmic(['baseboard', 'get', 'manufacturer'])
        return name

    def _kernel_version(self):
        '''
        Returns the kernel version, for example: "8"
        '''
        return platform.uname()[2]

    def _storage_info(self, path='c:'):
        '''
        Returns the amount of free space for given drive in bytes (int)
        '''
        if not path:
            path = "c:"  # WARNING check if it's valid for disk_usage()

        if sys.version_info >= (3, 3):
            try:
                from shutil import disk_usage
            except ImportError:
                pass
            else:
                return disk_usage(path).free

        # if python version is below 3.3 or shutil import failed
        drive = path.split(':')[0] + ":"  # ensure only drive letter
        cmd = ['fsutil', 'volume', 'diskfree', drive]
        p = Popen(cmd, stderr=PIPE, stdout=PIPE)
        data = p.communicate()[0]
        splits = data.strip().splitlines()
        free_bytes = splits[2].split(':')[-1].strip()
        return int(free_bytes)

    def _memory_info(self):
        """Return total system memory (RAM) in bytes (int)
        """
        b = self._call_wmic(['computersystem', 'get', 'TotalPhysicalMemory'])
        return int(b)

    def _screen_resolution(self):
        '''
        Returns the screen resolution for example: "(1366, 768)"
        '''
        return (win_api_defs.GetSystemMetrics(0),
                win_api_defs.GetSystemMetrics(1))


def instance():
    return WindowsSysinfo()
