import platform
import subprocess
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo


class OSXSysinfo(Sysinfo):

    def _model_info(self):
        mi = Popen("system_profiler SPHardwareDataType | grep Model\ Identifier",
                   shell = True,
                   stdout = PIPE).communicate()[0]
        mi = mi.split('Model Identifier: ')[1]
        return mi

    def _system_info(self):
        return platform.system()

    def _platform_info(self):
        return platform.platform()

    def _processor_info(self):
        return platform.processor()

    def _version_info(self):
        return platform.mac_ver()

    def _architecture_info(self):
        return platform.architecture()

    def _device_name(self):
        return platform.uname()[1]

    def _manufacturer_name(self):
        mn = Popen('system_profiler SPUSBDataType | grep Manufacturer',
                   shell = True,
                   stdout = PIPE).communicate()[0]
        mn = mn.split('Manufacturer: ')
        mn = mn[1].split('\n')
        return mn[0]

    def _kernel_version(self):
        return platform.uname()[2]

    def _storage_info(self):

        si = Popen('system_profiler SPHardwareDataType | grep Memory',
                   shell = True,
                   stdout = PIPE).communicate()[0]
        si = si.split('Memory: ')[1].split(' ')[0]
        return si

    def _screen_dimension(self):
        sd = Popen('system_profiler SPDisplaysDataType | grep Resolution',
                   shell = True,
                   stdout = PIPE).communicate()[0]
        sd = sd.split('Resolution:')[1]
        sd = sd.split(' ')
        sd1 = sd[1]
        sd2 = sd[3]
        return (int(sd1), int(sd2))


def instance():
    return OSXSysinfo()
