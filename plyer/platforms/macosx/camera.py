import subprocess
from plyer.facades import Camera
from plyer.utils import whereis_exe


class SnapCamera(Camera):

    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = str(filename)
        subprocess.call(["imagesnap", self.filename])
        self.on_complete()

    def _take_video(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = str(filename)
        subprocess.call(["videosnap", "-p", "1280x720", "-w", 2, "-d",
                         "Built-in iSight", self.filename])
        self.on_complete()


class WacawCamera(Camera):

    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        try:
            name, extension = filename.split(".")
        except:
            extension = None
        if extension = "jpg":
            subprocess.call(["wacaw", "--jpeg", "--VGA", self.filename])
        elif extension = "png":
            subprocess.call(["wacaw", "--png", "--VGA", self.filename])
        elif extension = "tiff":
            subprocess.call(["wacaw", "--tiff", "--VGA", self.filename])
        elif extension = "gif":
            subprocess.call(["wacaw", "--gif", "--VGA", self.filename])
        elif extension = "bmp":
            subprocess.call(["wacaw", "--bmp", "--VGA", self.filename])
        elif extension = None:
            subprocess.call(["wacaw", "--jpeg", "--VGA",
                             self.filename + ".jpg"])
        self.on_complete()

    def _take_video(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        subprocess.call(["wacaw", "--video", "--VGA", self.filename])
        self.on_complete()


def instance():
    if whereis_exe('videosnap') and whereis_exe('imagesnap'):
        return SnapCamera()
    elif whereis_exe('wacaw'):
        return WacawCamera()
    return Camera()
