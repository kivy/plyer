import platform
import subprocess
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo


class LinuxSysinfo(Sysinfo):

    def _model_info(self):
        '''
        Returns the model info for example: "VirtualBox"
        '''
        command = 'cat /sys/devices/virtual/dmi/id/product_name '.split()
        p = Popen(command, stderr=PIPE, stdout=PIPE)
        sp = p.communicate()[0].decode('utf-8')[:-1]
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
        Returns the type of processor for example: "x86_64"
        '''
        return platform.processor()

    def _version_info(self):
        '''
        Returns the version of OS in a tuple for example:
        "Ubuntu 15.10 wily"
        '''
        return platform.version()

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
        command = 'cat /sys/devices/virtual/dmi/id/sys_vendor '.split()
        p = Popen(command, stderr=PIPE, stdout=PIPE)
        sp = p.communicate()[0].decode('utf-8')[:-1]
        return sp

    def _kernel_version(self):
        '''
        Returns the kernel version for example: "4.2.0-32-generic"
        '''
        return platform.uname()[2]

    def _storage_info(self):
        '''
        Returns the amount of storage (RAM) in GB. for example: "1.43 GB"
        '''
        meminfo = {}

        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()
        try:
            memory, unit = meminfo['MemTotal'].split(' ')
            if (unit.lower() == "kb"):
                return str(round(int(memory) / (1024.0 * 1024.0), 2)) + " GB"
            elif (unit.lower() == "mb"):
                return str(round(int(memory) / (1024.0), 2)) + " GB"
            elif (unit.lower() == "gb"):
                return str(int(memory)) + " GB"
        except:
            return str(meminfo['MemTotal'])

    def _screen_resolution(self):
        '''
        Returns the screen resolution for example: "[1920, 975]"
        '''
        sd = Popen('xrandr | grep "\*" | cut -d" " -f4',
                   shell=True,
                   stdout=PIPE).communicate()[0].decode('utf-8')

        a = sd.split('x')[0]
        b = sd.split('x')[1].split('\n')[0]
        return (int(a), int(b))


def instance():
    return LinuxSysinfo()
