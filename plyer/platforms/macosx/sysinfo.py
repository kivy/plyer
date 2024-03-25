import platform
import subprocess
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo


class OSXSysinfo(Sysinfo):

    def _model_info(self):
        '''
        Returns the model info for example: "MacBookPro11,4"
        '''
        mi = Popen("system_profiler SPHardwareDataType | grep Model\ " +
                   "Identifier",
                   shell=True,
                   stdout=PIPE).communicate()[0]
        mi = mi.decode('utf-8').split('Model Identifier: ')[1][:-1]
        return mi

    def _system_name(self):
        '''
        Returns the system's OS name for example: "Darwin"
        '''
        return platform.system()

    def _platform_info(self):
        '''
        Returns platform's name for ecample:
        "Darwin-15.5.0-x86_64-i386-64bit"
        '''
        return platform.platform()

    def _processor_info(self):
        '''
        Returns the type of processor for example: "i386"
        '''
        return platform.processor()

    def _version_info(self):
        '''
        Returns the version of OS in a tuple for example:
        "10.11.5 (",",") x84_64"
        '''
        return platform.mac_ver()

    def _architecture_info(self):
        '''
        Returns the architecture in a tuple for example: "('64bit', ")"
        '''
        return platform.architecture()

    def _device_name(self):
        '''
        Returns the device name for example: "Kuldeeps-MacBook-Pro.local"
        '''
        return platform.uname()[1]

    def _manufacturer_name(self):
        '''
        Returns the manufacturer's name for example: "Apple Inc."
        '''
        mn = Popen('system_profiler SPHardwareDataType|grep Chip',
                   shell=True,
                   stdout=PIPE).communicate()[0]

        mn = mn.decode('utf-8').split('Chip: ')
        mn = mn[1].split('\n')
        return mn[0].split(' ')[0]

    def _kernel_version(self):
        '''
        Returns the kernel version for example: "15.5.0"
        '''
        return platform.uname()[2]

    def _storage_info(self):
        '''
        Returns the amount of storage (RAM) in GB. for example: "16 GB"
        '''
        si = Popen('system_profiler SPHardwareDataType | grep Memory',
                   shell=True,
                   stdout=PIPE).communicate()[0].decode('utf-8')
        si = si.split('Memory: ')[1].split(' ')[0]
        return str(si) + " GB"

    def _screen_resolution(self):
        '''
        Returns the screen resolution for example: "[2880, 1800]"
        '''
        sd = Popen('system_profiler SPDisplaysDataType | grep Resolution',
                   shell=True,
                   stdout=PIPE).communicate()[0].decode('utf-8')
        sd = sd.split('Resolution:')[1]
        sd = sd.split(' ')
        sd1 = sd[1]
        sd2 = sd[3]
        return (int(sd1), int(sd2))


def instance():
    return OSXSysinfo()
