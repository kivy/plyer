'''
Linux Dirs Manager
-----------
'''

from plyer.facades import Dirs
# NOTE named imports
from os.path import expanduser, join as path_join 
from os import getenv

class LinuxDirs(Dirs):

    def _get_private(self, appname, version=None):
        path = getenv('XDG_CONFIG_HOME', expanduser("~/.config"))
        #path = path_join(path, appname) # doesn't seem to be needed
        if version:
            path = path_join(path, version)
        return path

    def _get_cache(self, appname, version=None):
        path = getenv('XDG_CACHE_HOME', expanduser('~/.cache'))
        #path = path_join(path, appname) # doesn't seem to be needed
        if version:
            path = path_join(path, version)
        return path


def instance():
    return LinuxDirs()
