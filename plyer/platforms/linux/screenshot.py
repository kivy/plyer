import subprocess
from plyer.facades import Screenshot
from plyer.utils import whereis_exe


class GnomeScreenshot(Screenshot):
    def __init__(self, file_path=None):
        default_path = 'test.jpg'
        super(GnomeScreenshot, self).__init__(file_path or default_path)

    def _take_shot(self):
        subprocess.call(["gnome-screenshot", "-d", "2", self.file_path])


class ImportScreenshot(Screenshot):
    def __init__(self, file_path=None):
        default_path = 'test.jpg'
        super(ImportScreenshot, self).__init__(file_path or default_path)

    def _take_shot(self):
        subprocess.call(["import", "-window", "root", self.file_path])


def instance():
    if whereis_exe('gnome-screenshot'):
        return GnomeScreenshot()
    elif whereis_exe('import'):
        return ImportScreenshot()
    return Screenshot()
