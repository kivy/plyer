import subprocess
from plyer.facades import Screenshot
from plyer.utils import whereis_exe
import Xlib
from Xlib import display, X
from PIL import Image


class XlibScreenshot(Screenshot):
    def __init__(self, file_path=None):
        default_path = 'screenshot.jpg'
        super(XlibScreenshot, self).__init__(file_path or default_path)

    def _take(self):
        resolution = Xlib.display.Display().screen().root.get_geometry()
        W = resolution.width
        H = resolution.height
        dsp = display.Display()
        root = dsp.screen().root
        raw = root.get_image(0, 0, W, H, X.ZPixmap, 0xffffffff)
        image = Image.frombytes("RGB", (W, H), raw.data, "raw", "BGRX")
        image.save(str(self.file_path))


def instance():
    return XlibScreenshot()
