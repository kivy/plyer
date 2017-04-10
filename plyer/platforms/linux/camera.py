import subprocess
from plyer.facades import Camera


class GstreamerCamera(Camera):

    def _take_picture(self, on_complete, filename=None):
        self.on_complete = on_complete
        self.filename = filename
        try:
            name, extension = filename.split(".")
        except ValueError:
            extension = None
        if extension == "jpg":
            subprocess.call(["gst-launch-1.0", "v4l2src", "num-buffers=1", "!",
                             "jpegenc", "!", "filesink",
                             "location=" + self.filename])
        elif extension == "png":
            subprocess.call(["gst-launch-1.0", "v4l2src", "num-buffers=1",
                             "!", "pngenc", "!", "filesink",
                             "location=" + self.filename])
        elif extension is None:
            subprocess.call(["gst-launch-1.0", "v4l2src", "num-buffers=1", "!",
                             "jpegenc", "!", "filesink",
                             "location=" + self.filename + ".jpg"])
        else:
            pass
        self.on_complete()

    def _take_video(self, on_complete, filename=None):
        self.on_complete = on_complete
        self.filename = filename
        try:
            name, extension = filename.split(".")
        except:
            extension = None
        if extension is None:
            subprocess.call(["gst-launch-1.0", "v4l2src", "!", "videoconvert",
                             "!", "jpegenc", "!", "avimux", "!", "filesink",
                             "location=" + self.filename + ".avi"])
        else:
            subprocess.call(["gst-launch-1.0", "v4l2src", "!", "videoconvert",
                             "!", "jpegenc", "!", "avimux", "!", "filesink",
                             "location=" + self.filename])
        self.on_complete()


def instance():
    return GstreamerCamera()
