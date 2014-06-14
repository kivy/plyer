from plyer.facades import Camera

from threading import Thread
from os.path import dirname, realpath
from os import unlink
import subprocess

imagesnap = dirname(realpath(__file__)) + "/bin/imagesnap"
        
class CaptureCameraImageSnap(Thread):
    def __init__(self, on_complete, filename):
        Thread.__init__(self)
        self.on_complete = on_complete
        self.filename = filename

    def _unlink(self):
        try:
            unlink(self.filename)
        except:
            pass

    def run(self):
        subprocess.check_call([imagesnap, self.filename], stdout=subprocess.PIPE)
        if(self.on_complete(self.filename)):
           self._unlink()

class OSXCamera(Camera):
    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        assert(filename is not None)
        
        CaptureCameraImageSnap(on_complete, filename).run()

def instance():
    return OSXCamera()
    