'''
iOS Dirs Manager
-----------
'''

from plyer.facades import Dirs
from os.path import expanduser, join as path_join

class IosDirs(Dirs):

    def _get_private(self, appname, version=None):
        path = expanduser('~/Library/Application Support')
        if version:
            path = path_join(path, version)
        return path

    def _get_cache(self, appname, version=None):
        path = expanduser('~/Library/Caches')
        if version:
            path = path_join(path, version)
        return path


def instance():
    return IosDirs()
