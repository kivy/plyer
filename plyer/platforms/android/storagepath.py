'''
Android Storage Path
--------------------
'''

from plyer.facades import StoragePath
from jnius import autoclass
from android import mActivity

Environment = autoclass('android.os.Environment')
Context = autoclass('android.content.Context')


class AndroidStoragePath(StoragePath):

    def _get_home_dir(self):
        return Environment.getDataDirectory().getAbsolutePath()

    def _get_external_storage_dir(self):
        return Environment.getExternalStorageDirectory().getAbsolutePath()

    def _get_root_dir(self):
        return Environment.getRootDirectory().getAbsolutePath()

    def _get_documents_dir(self):
        return Environment.getExternalStoragePublicDirectory(
            Environment.DIRECTORY_DOCUMENTS).getAbsolutePath()

    def _get_downloads_dir(self):
        return Environment.getExternalStoragePublicDirectory(
            Environment.DIRECTORY_DOWNLOADS).getAbsolutePath()

    def _get_videos_dir(self):
        return Environment.getExternalStoragePublicDirectory(
            Environment.DIRECTORY_MOVIES).getAbsolutePath()

    def _get_music_dir(self):
        return Environment.getExternalStoragePublicDirectory(
            Environment.DIRECTORY_MUSIC).getAbsolutePath()

    def _get_pictures_dir(self):
        return Environment.getExternalStoragePublicDirectory(
            Environment.DIRECTORY_PICTURES).getAbsolutePath()

    def _get_application_dir(self):
        return mActivity.getFilesDir().getParentFile().getParent()


def instance():
    return AndroidStoragePath()
