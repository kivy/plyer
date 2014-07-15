from subprocess import Popen, PIPE
from plyer.facades import UniqueID
from plyer.utils import whereis_exe


class LinuxUniqueID(UniqueID):
    def _get_uid(self):
        lshw_process = Popen(["lshw", "-quiet"], stdout=PIPE, stderr=PIPE)
        grep_process = Popen(["grep", "-m1", "serial:"],
            stdin=lshw_process.stdout, stdout=PIPE)
        lshw_process.stdout.close()
        output = grep_process.communicate()[0]

        if output:
            return output.split()[1]
        else:
            return None


def instance():
    import sys
    if whereis_exe('lshw'):
        return LinuxUniqueID()
    sys.stderr.write("lshw not found.")
    return UniqueID()
