import re
import os
import platform
import subprocess
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo


class LinuxSysinfo(Sysinfo):

    def _model_info(self):
        '''
        Returns the model info for example: "VirtualBox"
        '''
        command = ('cat', '/sys/devices/virtual/dmi/id/product_name')
        p = Popen(command, stderr=PIPE, stdout=PIPE)
        sp = p.communicate()[0]
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
        '''
        Returns the model and type of processor, for example:
        "GenuineIntel, Intel(R) Core(TM) i7 CPU 860 @ 2.80GHz, 4 cores, x86_64"
        '''
        info = platform.processor()
        try:
            command = ('cat', '/proc/cpuinfo')
            p = Popen(command, stderr=PIPE, stdout=PIPE)
            cat = p.communicate()[0]
        except:
            pass
        else:
            if cat:
                l = []
                data_ptrn = "[\t ]*:[\t ](?P<data>[^\t\n ]+" \
                            "(?:[\t ]+[^\n\t ]+)*)"
                vendor_ptrn = "vendor_id" + data_ptrn
                model_ptrn = "model name" + data_ptrn
                core_ptrn = "cpu cores\D*(?P<cores>\d+)[\t ]*\n"
                strip_ptrn = "(?:\t+|[ ]{2,})"
                m = re.search(vendor_ptrn, cat, re.IGNORECASE)
                if m:
                    l.append(m.group('data'))
                m = re.search(model_ptrn, cat, re.IGNORECASE)
                if m:
                    l.append(m.group('data'))
                m = re.search(core_ptrn, cat, re.IGNORECASE)
                if m:
                    cores = int(m.group('cores'))
                    if cores <= 1:
                        l.append("1 core")
                    else:
                        l.append("{0} cores".format(cores))
                l.append(info)
                info = ", ".join(l)
                info = re.sub(strip_ptrn, ' ', info)
        return info

    def _version_info(self):
        '''
        Returns the version of OS in a tuple for example:
        "Ubuntu 15.10 wily"
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

    def _manufacturer_name(self):
        '''
        Returns the manufacturer's name for example: "innotek GmnH"
        '''
        command = ('cat', '/sys/devices/virtual/dmi/id/sys_vendor')
        p = Popen(command, stderr=PIPE, stdout=PIPE)
        sp = p.communicate()[0]

        # if system manufacturer is not set, return system board manufacturer
        if sp.strip().lower() in ('system manufacturer', ''):
            command = ('cat', '/sys/devices/virtual/dmi/id/board_vendor')
            p = Popen(command, stderr=PIPE, stdout=PIPE)
            board = p.communicate()[0]
            if board:
                return board
        return sp

    def _kernel_version(self):
        '''
        Returns the kernel version for example: "4.2.0-32-generic"
        '''
        return platform.uname()[2]

    def _storage_info(self):
        # Return available storage space in bytes (integer)
        # On Linux stats for ~/ (user's home) as making more sense if app
        # is to store data there. Notice that Linux installations often
        # have separate /home partition
        stat = os.statvfs(os.path.expanduser('~/'))
        free_bytes = stat.f_bavail * stat.f_frsize
        return int(free_bytes)

    def _memory_info(self):
        '''
        Returns the total amount of memory (RAM) in bytes.
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
            a = sd.split('x')[0]
            b = sd.split('x')[1].split('\n')[0]
        except:
            a, b = (0, 0)  # if parsing failed return something at leasts
        return (int(a), int(b))


def instance():
    return LinuxSysinfo()
