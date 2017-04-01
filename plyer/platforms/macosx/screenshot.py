import subprocess
from plyer.facades import ScreenShot
from plyer.utils import whereis_exe


class OSXScreenShot(ScreenShot):

    def _take_shot(self, on_complete, filename=None):
        self.on_complete = on_complete
        self.filename = str(filename)
        subprocess.call(["screencapture", "-T", "2", self.filename])
        self.on_complete()


def instance():
    if whereis_exe('screencapture'):
        return OSXScreenShot()
    return ScreenShot()
