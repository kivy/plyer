import re
import os
import sys
import platform
import subprocess
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo


class LinuxSysinfo(Sysinfo):

    def _model_info(self, alias=True):
        '''
        Returns the model info for example: "VirtualBox"
        '''
        command = ('cat', '/sys/devices/virtual/dmi/id/product_name')
        p = Popen(command, stderr=PIPE, stdout=PIPE)
        sp = p.communicate()[0].strip()

        if alias and sp.lower().strip() in ('system product name', ''):
            command = ('cat', '/sys/devices/virtual/dmi/id/board_name')
            p = Popen(command, stderr=PIPE, stdout=PIPE)
            board = p.communicate()[0].strip()
            if board:
                return "{0} ({1})".format(self._device_name(), board)
        return sp

    def _system_name(self):
        '''
        Returns the system's OS name for example: "Linux"
        '''
        return platform.system()

    def _platform_info(self):
        '''
        Returns platform's name for example:
        "Lunix-4.2.0-36-generic-x86_64-with-Ubuntu-15.10-wily"
        '''
        return platform.platform()

    def _processor_info(self):
        """Returns the information of processor as tuple-like object of
        * **model** *(str)*: CPU model name or '' (not implemented)
        * **manufacturer** *(str)*: manufacturer name
        * **arch** *(str)*: architecture info
        * **cores** *(int)*: number of physical cores or None (not implemented)
        for example:
        cpu_namedtuple(model='', manufacturer='qcom',
                       cores=None, arch='armeabi-v7a')
        """
        try:
            command = ('cat', '/proc/cpuinfo')
            p = Popen(command, stderr=PIPE, stdout=PIPE)
            cat = p.communicate()[0]
        except:
            return self.CpuNamedTuple(model=platform.processor(),
                                      manufacturer='',
                                      cores=None,
                                      arch=platform.machine())
        else:
            l = []
            data_ptrn = "[\t ]*:[\t ](?P<data>[^\t\n ]+" \
                        "(?:[\t ]+[^\n\t ]+)*)"
            vendor_ptrn = "vendor_id" + data_ptrn
            model_ptrn = "model name" + data_ptrn
            core_ptrn = "cpu cores\D*(?P<cores>\d+)[\t ]*\n"
            strip_ptrn = "(?:\t+|[ ]{2,})"
            m = re.search(vendor_ptrn, cat, re.IGNORECASE)
            if m:
                manf = m.group('data')
            else:
                manf = ''

            m = re.search(model_ptrn, cat, re.IGNORECASE)
            if m:
                model = m.group('data')
                model = re.sub(strip_ptrn, ' ', model)
            else:
                model = ''

            m = re.search(core_ptrn, cat, re.IGNORECASE)
            if m:
                cores = int(m.group('cores'))
            else:
                cores = None

            return self.CpuNamedTuple(model=model, manufacturer=manf,
                                      cores=cores, arch=platform.machine())

    def _version_info(self):
        '''
        Returns the version of OS in a tuple for example:
        ("Ubuntu", "15.10", "wily")
        '''
        return platform.dist()

    def _architecture_info(self):
        '''
        Returns the architecture in a tuple for example: "('64bit', 'ELF')"
        '''
        return platform.architecture()

    def _device_name(self):
        '''
        Returns the device name for example: "kuldeep-virtualbox"
        '''
        return platform.uname()[1]

    def _manufacturer_name(self, alias=True):
        '''
        Returns the manufacturer's name for example: "innotek GmnH"
        '''
        command = ('cat', '/sys/devices/virtual/dmi/id/sys_vendor')
        p = Popen(command, stderr=PIPE, stdout=PIPE)
        sp = p.communicate()[0].strip()

        # if system manufacturer is not set, return system board manufacturer
        if alias and sp.lower() in ('system manufacturer', ''):
            command = ('cat', '/sys/devices/virtual/dmi/id/board_vendor')
            p = Popen(command, stderr=PIPE, stdout=PIPE)
            board = p.communicate()[0].strip()
            if board:
                return board
        return sp

    def _kernel_version(self):
        '''
        Returns the kernel version for example: "4.2.0-32-generic"
        '''
        return platform.uname()[2]

    def _storage_info(self, path=None):
        """ Return available storage space in bytes (int).
        default path is user's home, expand user is performed on path
        * NOTE that Linux installations often have separate /home partition
        """
        if path:
            path = os.path.expanduser(path)
        else:
            path = os.path.expanduser('~/')

        if sys.version_info >= (3, 3):
            try:
                from shutil import disk_usage
            except ImportError:
                pass
            else:
                return disk_usage(path).free

        # if python version is below 3.3 or import failure
        stat = os.statvfs(path)
        free_bytes = stat.f_bavail * stat.f_frsize
        return int(free_bytes)

    def _memory_info(self):
        '''
        Returns the total amount of memory (RAM) in bytes (int).
        '''
        meminfo = {}

        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()
        try:
            memory, unit = meminfo['MemTotal'].split(' ')
            memory = int(memory)
            if (unit.lower() == "kb"):
                memory = memory * 1024
            elif (unit.lower() == "mb"):
                memory = memory * (1024 ** 2)
            elif (unit.lower() == "gb"):
                memory *= memory * (1024 ** 3)
        except Exception as ex:
            print('Exception with memory parsing: {0}'.format(ex))
            return str(meminfo['MemTotal'])
        return memory

    def _screen_resolution(self):
        '''
        Returns the screen resolution as tuple for example: "(1920, 975)"
        '''
        sd = Popen('xrandr | grep "\*" | cut -d" " -f4',
                   shell=True,
                   stdout=PIPE).communicate()[0]

        try:
            splits = sd.split('x')
            a = splits[0]
            b = splits[1].split('\n')[0]
        except:
            a, b = (0, 0)  # if parsing failed return something at leasts
        return (int(a), int(b))


def instance():
    return LinuxSysinfo()
