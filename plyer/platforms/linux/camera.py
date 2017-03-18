import subprocess
from plyer.facades import Camera


class LinuxCamera(Camera):

    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        try:
            name, extension = filename.split(".")
        except:
            extension = None
        if extension = "jpg":
            subprocess.call(["gst-launch", "v4l2src", "num-buffers=1", "!",
                             "jpegenc", "!", "filesink",
                             "location=" + self.filename])
        elif extension = "png":
            subprocess.call(["gst-launch", "v4l2src", "num-buffers=1",
                             "!", "pngenc", "!", "filesink",
                             "location=" + self.filename])
        elif extension = None:
            subprocess.call(["gst-launch", "v4l2src", "num-buffers=1", "!",
                             "jpegenc", "!", "filesink",
                             "location=" + self.filename + ".jpg"])
        else:
            pass
        self.on_complete()

    def _take_video(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        try:
            name, extension = filename.split(".")
        except:
            extension = None
        if extension = None:
            subprocess.call(["gst-launch", "v4l2src", "!", "ffmpegcolorspace",
                             "!", "jpegenc", "!", "avimux", "!", "filesink",
                             "location=" + self.filename + ".avi"])
        else:
            subprocess.call(["gst-launch", "v4l2src", "!", "ffmpegcolorspace",
                             "!", "jpegenc", "!", "avimux", "!", "filesink",
                             "location=" + self.filename])
        self.on_complete()


def instance():
    return LinuxCamera()
