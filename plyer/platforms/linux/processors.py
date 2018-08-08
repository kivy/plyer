from subprocess import Popen, PIPE
from plyer.facades import Processors
from plyer.utils import whereis_exe

from os import environ


class LinuxProcessors(Processors):
    def _cpus(self):
        old_lang = environ.get('LANG', '')
        environ['LANG'] = 'C'

        cpus = {
            'physical': None,  # cores
            'logical': None    # cores * threads
        }

        logical = Popen(
            ['nproc', '--all'],
            stdout=PIPE
        )
        output = logical.communicate()[0].decode('utf-8').strip()

        environ['LANG'] = old_lang
        if output:
            cpus['logical'] = int(output)
        return cpus


def instance():
    import sys
    if whereis_exe('nproc'):
        return LinuxProcessors()
    sys.stderr.write("nproc not found.")
    return Processors()
