import subprocess as sp
from plyer.facades import Camera


class LinuxCamera(Camera):

    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        sp.call(["gst-launch", "v4l2src", "num-buffers=1",
                 "!", "jpegenc", "!", "filesink",
                 "location="+self.filename+".jpg"])
        self.on_complete()

    def _take_video(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        sp.call(["gst-launch", "v4l2src", "!", "ffmpegcolorspace",
                 "!", "jpegenc", "!", "avimux", "!", "filesink",
                 "location="+self.filename+".avi"])
        self.on_complete()


def instance():
    return LinuxCamera()
