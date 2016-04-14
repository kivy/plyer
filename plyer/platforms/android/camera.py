from . import activity
from os import unlink
from jnius import autoclass, cast
from plyer.facades import Camera

Intent = autoclass('android.content.Intent')
MediaStore = autoclass('android.provider.MediaStore')
Uri = autoclass('android.net.Uri')


class AndroidCamera(Camera):

    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        activity.unbind(on_activity_result=self._on_activity_result)
        activity.bind(on_activity_result=self._on_activity_result)
        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        uri = Uri.parse('file://' + filename)
        parcelable = cast('android.os.Parcelable', uri)
        intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable)
        activity.startActivityForResult(intent, 0x123)

    def _take_video(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        activity.unbind(on_activity_result=self._on_activity_result)
        activity.bind(on_activity_result=self._on_activity_result)
        intent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
        uri = Uri.parse('file://' + filename)
        parcelable = cast('android.os.Parcelable', uri)
        intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable)

        # 0 = low quality, suitable for MMS messages,
        # 1 = high quality
        intent.putExtra(MediaStore.EXTRA_VIDEO_QUALITY, 1)
        activity.startActivityForResult(intent, 0x123)

    def _on_activity_result(self, requestCode, resultCode, intent):
        if requestCode != 0x123:
            return
        activity.unbind(on_activity_result=self._on_activity_result)
        if self.on_complete(self.filename):
            self._unlink(self.filename)

    def _unlink(self, fn):
        try:
            unlink(fn)
        except:
            pass


def instance():
    return AndroidCamera()
