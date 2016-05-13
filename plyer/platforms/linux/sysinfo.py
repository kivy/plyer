import platform
import subprocess
from subprocess import Popen, PIPE
from plyer.facades import Sysinfo


class LinuxSysinfo(Sysinfo):

    def _model_info(self):
        command = 'cat /sys/devices/virtual/dmi/id/product_name '.split()
        p = Popen(command, stderr=PIPE, stdout=PIPE)
        sp = p.communicate()[0]
        return sp

    def _system_info(self):
        return platform.system()

    def _platform_info(self):
        return platform.platform()

    def _processor_info(self):
        return platform.processor()

    def _version_info(self):
        return platform.dist()

    def _architecture_info(self):
        return platform.architecture()

    def _device_name(self):
        return platform.uname()[1]

    def _manufacturer_name(self):
        command = 'cat /sys/devices/virtual/dmi/id/sys_vendor '.split()
        p = Popen(command, stderr=PIPE, stdout=PIPE)
        sp = p.communicate()[0]
        return sp

    def _kernel_version(self):
        return platform.uname()[2]

    def _storage_info(self):
        meminfo = {}

        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()
        return str(meminfo['MemTotal'])

    def _screen_dimension(self):
        sd = Popen('xrandr | grep "\*" | cut -d" " -f4',
                   shell=True,
                   stdout=PIPE).communicate()[0]

        a = sd.split('x')[0]
        b = sd.split('x')[1].split('\n')[0]
        return (int(a), int(b))


def instance():
    return LinuxSysinfo()
