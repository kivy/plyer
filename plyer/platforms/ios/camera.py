from pyobjus import autoclass
from pyobjus import protocol
from os import unlink
from plyer.facades import Camera

from plyer.utils import reify


class iOSCamera(Camera):

    @reify
    def photos(self):
        # pyPhotoLibrary is a ios recipe/module that interacts with the gallery
        # and the  camera on ios.
        from photolibrary import PhotosLibrary
        return PhotosLibrary()

    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        photos = self.photos

        if not photos.isCameraAvailable():
            # no camera hardware
            return False

        photos.bind(on_image_captured=self.capture_callback)
        self._capture_filename = filename
        photos.capture_image(filename)
        return True

    def capture_callback(self, photolibrary):
        # Image was choosen

        # unbind
        self.photos.unbind(on_image_captured=self.capture_callback)

        if self.on_complete(self.filename):
            self._unlink(self.filename)

    def _take_video(self, on_complete, filename=None):
        assert(on_complete is not None)
        raise NotImplementedError

    def _unlink(self, fn):
        try:
            unlink(fn)
        except Exception:
            print('Could not remove photo!')


def instance():
    return iOSCamera()
