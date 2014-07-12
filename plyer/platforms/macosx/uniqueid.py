from subprocess import Popen, PIPE
from plyer.facades import UniqueID


class OSXUniqueID(UniqueID):
    def _get_uid(self):
        ioreg_process = Popen(["ioreg", "-l"], stdout=PIPE)
        grep_process = Popen(["grep", "IOPlatformSerialNumber"],
            stdin=ioreg_process.stdout, stdout=PIPE)
        ioreg_process.stdout.close()
        output = grep_process.communicate()[0]

        if output:
            return output.split()[3][1:-1]
        else:
            return None


def instance():
    return OSXUniqueID()
