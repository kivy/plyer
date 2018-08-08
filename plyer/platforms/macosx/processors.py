from subprocess import Popen, PIPE
from plyer.facades import Processors
from plyer.utils import whereis_exe


class OSXProcessors(Processors):
    def _cpus(self):
        cpus = {
            'physical': None,  # cores
            'logical': None    # cores * threads
        }

        physical = Popen(
            ['sysctl', '-n', 'hw.physicalcpu_max'],
            stdout=PIPE
        )
        output = physical.communicate()[0].decode('utf-8').strip()
        if output:
            cpus['physical'] = int(output)

        logical = Popen(
            ['sysctl', '-n', 'hw.logicalcpu_max'],
            stdout=PIPE
        )
        output = logical.communicate()[0].decode('utf-8').strip()
        if output:
            cpus['logical'] = int(output)
        return cpus


def instance():
    import sys
    if whereis_exe('sysctl'):
        return OSXProcessors()
    sys.stderr.write('sysctl not found.')
    return Processors()
