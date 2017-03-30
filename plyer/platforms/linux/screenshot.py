import subprocess
from plyer.facades import ScreenShot
from plyer.utils import whereis_exe


class GnomeScreenShot(ScreenShot):

    def _take_shot(self, on_complete, filename=None):
        self.on_complete = on_complete
        self.filename = str(filename)
        subprocess.call(["gnome-screenshot", "-d", "2", self.filename])
        self.on_complete()


class ImportScreenShot(ScreenShot):

    def _take_shot(self, on_complete, filename=None):
        self.on_complete = on_complete
        self.filename = str(filename)
        subprocess.call(["import", "-window", "root", self.filename])
        self.on_complete()


def instance():
    if whereis_exe('gnome-screenshot'):
        return GnomeScreenShot()
    elif whereis_exe('import'):
        return ImportScreenShot()
    return ScreenShot()
