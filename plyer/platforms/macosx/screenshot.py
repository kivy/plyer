import subprocess
from plyer.facades import ScreenShot
from plyer.utils import whereis_exe


class OSXScreenShot(ScreenShot):
    def __init__(self, file_path=None):
        default_path = 'test.jpg'
        super(OSXScreenShot, self).__init__(file_path or default_path)

    def _take_shot(self):
        subprocess.call(["screencapture", "-T", "2", self.filename])


def instance():
    if whereis_exe('screencapture'):
        return OSXScreenShot()
    else:
        return ScreenShot()
