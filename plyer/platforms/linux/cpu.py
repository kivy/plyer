from subprocess import Popen, PIPE
from plyer.facades import CPU
from plyer.utils import whereis_exe

from os import environ


class LinuxCPU(CPU):
    def _sockets(self):
        # physical CPU sockets (or slots) on motherboard
        sockets = []  # list of CPU ids from kernel

        # open Linux kernel data file for CPU
        with open('/proc/cpuinfo', 'rb') as fle:
            lines = fle.readlines()

        # go through the lines and obtain physical CPU ids
        for line in lines:
            line = line.decode('utf-8')
            if 'physical id' not in line:
                continue
            cpuid = line.split(':')[1].strip()
            sockets.append(cpuid)

        # total sockets is the length of unique CPU ids from kernel
        sockets = len(set(sockets))
        return sockets

    def _physical(self):
        # cores
        physical = []  # list of CPU ids from kernel

        # open Linux kernel data file for CPU
        with open('/proc/cpuinfo', 'rb') as fle:
            lines = fle.readlines()

        # go through the lines and obtain CPU core ids
        for line in lines:
            line = line.decode('utf-8')
            if 'core id' not in line:
                continue
            cpuid = line.split(':')[1].strip()
            physical.append(cpuid)

        # total cores (socket * core per socket)
        # is the length of unique CPU core ids from kernel
        physical = len(set(physical))
        return physical

    def _logical(self):
        # cores * threads
        logical = None
        old_lang = environ.get('LANG', '')
        environ['LANG'] = 'C'

        _logical = Popen(['nproc', '--all'], stdout=PIPE)
        output = _logical.communicate()[0].decode('utf-8').strip()
        if output:
            logical = int(output)

        environ['LANG'] = old_lang
        return logical


def instance():
    import sys
    if whereis_exe('nproc'):
        return LinuxCPU()
    sys.stderr.write("nproc not found.")
    return CPU()
