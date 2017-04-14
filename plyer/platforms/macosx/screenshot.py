import subprocess
from plyer.facades import Screenshot
from plyer.utils import whereis_exe


class OSXScreenshot(ScreenShot):
    def __init__(self, file_path=None):
        default_path = 'screenshot.jpg'
        super(OSXScreenshot, self).__init__(file_path or default_path)

    def _take(self):
        subprocess.call(["screencapture", "-T", "2", self.file_path])


def instance():
    if whereis_exe('screencapture'):
        return OSXScreenshot()
    else:
        return Screenshot()
