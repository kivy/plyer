import subprocess
from plyer.facades import ScreenShot
from plyer.utils import whereis_exe


class GnomeScreenShot(ScreenShot):
    def __init__(self, file_path=None):
        default_path = 'test.jpg'
        super(GnomeScreenShot, self).__init__(file_path or default_path)

    def _take_shot(self):
        subprocess.call(["gnome-screenshot", "-d", "2", self.file_path])


class ImportScreenShot(ScreenShot):
    def __init__(self, file_path=None):
        default_path = 'test.jpg'
        super(ImportScreenShot, self).__init__(file_path or default_path)

    def _take_shot(self):
        subprocess.call(["import", "-window", "root", self.file_path])


def instance():
    if whereis_exe('gnome-screenshot'):
        return GnomeScreenShot()
    elif whereis_exe('import'):
        return ImportScreenShot()
    return ScreenShot()
