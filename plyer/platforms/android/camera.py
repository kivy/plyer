import android
import android.activity
from os import remove
from jnius import autoclass, cast, JavaException
from plyer.facades import Camera
from plyer.platforms.android import activity

Intent = autoclass('android.content.Intent')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
MediaStore = autoclass('android.provider.MediaStore')
Uri = autoclass('android.net.Uri')
File = autoclass('java.io.File')
FileProvider = autoclass('android.support.v4.content.FileProvider')


class AndroidCamera(Camera):

    FILEPROVIDER_AUTHORITY = None

    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        android.activity.unbind(on_activity_result=self._on_activity_result)
        android.activity.bind(on_activity_result=self._on_activity_result)
        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        uri = self._get_uri_for_file(filename)
        parcelable = cast('android.os.Parcelable', uri)
        intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable)
        activity.startActivityForResult(intent, 0x123)

    def _take_video(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        android.activity.unbind(on_activity_result=self._on_activity_result)
        android.activity.bind(on_activity_result=self._on_activity_result)
        intent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
        uri = self._get_uri_for_file(filename)
        parcelable = cast('android.os.Parcelable', uri)
        intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable)

        # 0 = low quality, suitable for MMS messages,
        # 1 = high quality
        intent.putExtra(MediaStore.EXTRA_VIDEO_QUALITY, 1)
        activity.startActivityForResult(intent, 0x123)

    def _on_activity_result(self, requestCode, resultCode, intent):
        if requestCode != 0x123:
            return
        android.activity.unbind(on_activity_result=self._on_activity_result)
        if self.on_complete(self.filename):
            self._remove(self.filename)

    def _remove(self, fn):
        try:
            remove(fn)
        except OSError:
            pass

    def _get_uri_for_file(self, filename):
        if self.FILEPROVIDER_AUTHORITY is None:
            # default behavior, backward-compatible: works with Android <= 9
            return Uri.parse('file://' + filename)
        #
        # For Android >= 10, we need to declare a FileProvider in
        # AndroidManifest and set plyer.camera.FILEPROVIDER_AUTHORITY accordingly
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        ctx = currentActivity.getApplicationContext()
        try:
            return FileProvider.getUriForFile(ctx, self.FILEPROVIDER_AUTHORITY,
                                              File(filename))
        except JavaException as exc:
            raise Exception(
                f'Cannot get a uri for filename {filename} for the Fileprovider '
                f'authority {self.FILEPROVIDER_AUTHORITY}.  This probably means that '
                f'FILE_PROVIDER_PATHS is not configured correctly in '
                f'AndroidManifest.xml and/or you need to change the value of '
                f'plyer.camera.FILEPROVIDER_AUTHORITY'
            )
        return uri


def instance():
    return AndroidCamera()
