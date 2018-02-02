'''
MacOS X Storage Path
--------------------
'''

import os.path
from plyer.facades import StoragePath
from plyer.platforms.macosx.libs import osx_paths

# Directory constants (NSSearchPathDirectory enumeration)
NSApplicationDirectory = 1
NSDocumentDirectory = 9
NSDownloadsDirectory = 15
NSMoviesDirectory = 17
NSMusicDirectory = 18
NSPicturesDirectory = 19


class OSXStoragePath(StoragePath):
    def _get_home_dir(self):
        return os.path.expanduser('~')

    def _get_external_storage_dir(self):
        return 'Method not implemented for current platform.'

    def _get_root_dir(self):
        return '/'

    def _get_documents_dir(self):
        return osx_paths.NSIterateSearchPaths(NSDocumentDirectory)

    def _get_downloads_dir(self):
        return osx_paths.NSIterateSearchPaths(NSDownloadsDirectory)

    def _get_videos_dir(self):
        return osx_paths.NSIterateSearchPaths(NSMoviesDirectory)

    def _get_music_dir(self):
        return osx_paths.NSIterateSearchPaths(NSMusicDirectory)

    def _get_pictures_dir(self):
        return osx_paths.NSIterateSearchPaths(NSPicturesDirectory)

    def _get_application_dir(self):
        return osx_paths.NSIterateSearchPaths(NSApplicationDirectory)


def instance():
    return OSXStoragePath()
