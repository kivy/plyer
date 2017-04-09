import subprocess
from plyer.facades import Screenshot
from plyer.utils import whereis_exe


class XwdScreenshot(Screenshot):
    def __init__(self, file_path=None):
        default_path = 'screenshot.jpg'
        super(XwdScreenshot, self).__init__(file_path or default_path)

    def _take(self):
        subprocess.call(["xwd", "-root", "-out", "screenshot.xwd"])
        subprocess.call(["convert", "screenshot.xwd", self.file_path])
        subprocess.call(["rm", "screenshot.xwd"])


def instance():
    if whereis_exe('xwd') and whereis_exe('convert'):
        return XwdScreenshot()
    else:
        return Screenshot()
