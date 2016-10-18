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
        """
            requires WRITE_EXTERNAL_STORAGE permission for some versions
        """
        context = activity.getApplicationContext()
        return context.getExternalCacheDir().getPath()



def instance():
    return AndroidDirs()
