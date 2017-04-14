from PIL import ImageGrab
from plyer.facades import Screenshot


class PILScreenshot(Screenshot):
    def __init__(self, file_path=None):
        default_path = 'screenshot.jpg'
        super(PILScreenshot, self).__init__(file_path or default_path)

    def _take(self):
        img = ImageGrab.grab()
        img.save(str(self.file_path))


def instance():
    return PILScreenshot()
