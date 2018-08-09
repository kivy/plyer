from subprocess import Popen, PIPE
from plyer.facades import CPU
from plyer.utils import whereis_exe

from os import environ


class LinuxProcessors(CPU):
    def _cpus(self):
        old_lang = environ.get('LANG', '')
        environ['LANG'] = 'C'

        cpus = {
            'physical': None,  # cores
            'logical': None    # cores * threads
        }

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
        # is the length of unique CPU ids from kernel
        physical = len(set(physical))
        cpus['physical'] = physical

        logical = Popen(
            ['nproc', '--all'],
            stdout=PIPE
        )
        output = logical.communicate()[0].decode('utf-8').strip()

        if output:
            cpus['logical'] = int(output)

        environ['LANG'] = old_lang
        return cpus


def instance():
    import sys
    if whereis_exe('nproc'):
        return LinuxProcessors()
    sys.stderr.write("nproc not found.")
    return CPU()
