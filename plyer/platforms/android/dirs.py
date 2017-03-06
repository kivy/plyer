'''
Android Dirs Manager
-----------
'''

from plyer.facades import Dirs
from plyer.platforms.android import activity

class AndroidDirs(Dirs):

    def _get_private(self, appname=None, version=None):
        context = activity.getApplicationContext()
        return context.getFilesDir().getPath()

    def _get_cache(self, appname=None, version=None):
        """ wrapper for Android getExternalCacheDir()
            Requires `WRITE_EXTERNAL_STORAGE` permission for some versions.
        """
        context = activity.getApplicationContext()
        return context.getExternalCacheDir().getPath()

    def _get_internal_cache(self, appname=None, version=None):
        """ wrapper for Android getCacheDir()
            Returns the absolute path to the application specific cache
            directory on the filesystem. These files will be ones that
            get deleted first when the device runs low on storage.
            There is no guarantee when these files will be deleted.
            Does not require any permissions.
            Suitable for small files (1MB) according to Google
            guidlines.
        """
        context = activity.getApplicationContext()
        return context.getCacheDir().getPath()

def instance():
    return AndroidDirs()
