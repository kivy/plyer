from subprocess import Popen, PIPE
from plyer.facades import CPU
from plyer.utils import whereis_exe


class OSXCPU(CPU):
    def _physical(self):
        # cores
        physical = None

        _physical = Popen(
            ['sysctl', '-n', 'hw.physicalcpu_max'],
            stdout=PIPE
        )
        output = _physical.communicate()[0].decode('utf-8').strip()
        if output:
            physical = int(output)
        return physical

    def _logical(self):
        # cores * threads
        logical = None

        _logical = Popen(
            ['sysctl', '-n', 'hw.logicalcpu_max'],
            stdout=PIPE
        )
        output = _logical.communicate()[0].decode('utf-8').strip()
        if output:
            logical = int(output)
        return logical


def instance():
    import sys
    if whereis_exe('sysctl'):
        return OSXCPU()
    sys.stderr.write('sysctl not found.')
    return CPU()
