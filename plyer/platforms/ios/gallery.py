from pyobjus import autoclass
from pyobjus import protocol
from os import unlink
from plyer.facades import Gallery
from plyer.utils import reify


class iOSGallery(Gallery):

    def __init__(self, **kwargs):
        super(iOSGallery, self).__init__(kwargs)
        self._create_nomedia()

    def _create_nomedia(self):
        if platform != 'android':
            return

        nfile = self.get_temporary_dir() + '/.nomedia'
        if exists(nfile):
            return

        f = open(nfile, 'wr')
        f.write('')
        f.close()

    @reify
    def photos(self):
        # pyPhotoLibrary is a ios recipe/module that interacts with the gallery
        # and the  camera on ios.
        from photolibrary import PhotosLibrary
        return PhotosLibrary()

    def _choose_image(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        photos = self.photos

        photos.bind(on_image_captured=self.capture_callback)
        photos.bind(on_capture_cancelled=self.capture_cancelled)
        self._capture_filename = filename
        photos.chooseFromGallery(filename, type='image')

    def capture_callback(self, photolibrary):
        # Image was choosen

        # unbind
        self.photos.unbind(
            on_image_captured=self.capture_callback,
            on_capture_cancelled=self.capture_cancelled)

        if self.on_complete(self.filename):
            self._unlink(self.filename)

    def capture_cancelled(selfi, *args):
        # Image Selection Cancelled

        # unbind
        self.photos.unbind(
            on_image_captured=self.capture_callback,
            on_capture_cancelled=self.capture_cancelled)

        self.on_complete(self.filename, finished=True)
        #self._unlink(self.filename)

    def _choose_video(self, on_complete, filename=None):
        assert(on_complete is not None)
        return

    def _unlink(self, fn):
        try:
            unlink(fn)
        except:
            pass


def instance():
    return iOSGallery()
