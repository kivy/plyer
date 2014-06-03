try:
    import opencv as cv
except ImportError:
    try:
        import cv2.cv as cv
    except ImportError:
        import cv

from threading import Thread as thread
from os import unlink
from plyer.facades import Camera
        
class CaptureCameraOpenCV(thread):
    def __init__(self, on_complete, filename, camIndex=0):
        self.filename = filename
        self.on_complete = on_complete
        self._camIndex = camIndex
        self._device = None
        super(CaptureCameraOpenCV, self).__init__()

    def _unlink(self, fn):
        try:
            unlink(fn)
        except:
            pass

    def start(self):
        self.capture = cv.CaptureFromCAM(self._camIndex)
        cv.NamedWindow("Camera", cv.CV_WINDOW_NORMAL)
        self.run()

    def run(self):
        # and wait!
        while (True):
            frame = cv.QueryFrame(self.capture)
            if(frame):
                cv.ShowImage("Press any key to capture...", frame)
            if(cv.WaitKey(10) != -1):
                break

        cv.SaveImage(self.filename, frame)
        cv.DestroyAllWindows()

        if(self.on_complete(self.filename)):
            self._unlink(self.filename)

class LinuxCamera(Camera):
    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        assert(filename is not None)

        CaptureCameraOpenCV(on_complete, filename).start()

def instance():
    return LinuxCamera()
    