'''
MacOS X Storage Path
--------------------
'''

from plyer.facades import StoragePath
from pyobjus import autoclass

NSFileManager = autoclass('NSFileManager')

# Directory constants (NSSearchPathDirectory enumeration)
NSApplicationDirectory = 1
NSDocumentDirectory = 9
NSDownloadsDirectory = 15
NSMoviesDirectory = 17
NSMusicDirectory = 18
NSPicturesDirectory = 19
NSDesktopDirectory = 12


def _nsstring_to_str(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value


class OSXStoragePath(StoragePath):

    def __init__(self):
        self.defaultManager = NSFileManager.defaultManager()

    def _get_home_dir(self):
        home_dir_NSURL = self.defaultManager.homeDirectoryForCurrentUser
        return _nsstring_to_str(home_dir_NSURL.absoluteString.UTF8String())

    def _get_external_storage_dir(self):
        return 'Method not implemented for current platform.'

    def _get_root_dir(self):
        return '/'

    def _get_documents_dir(self):
        return _nsstring_to_str(
            self.defaultManager.URLsForDirectory_inDomains_(
                NSDocumentDirectory, 1
            ).firstObject().absoluteString.UTF8String()
        )

    def _get_downloads_dir(self):
        return _nsstring_to_str(
            self.defaultManager.URLsForDirectory_inDomains_(
                NSDownloadsDirectory, 1
            ).firstObject().absoluteString.UTF8String()
        )

    def _get_videos_dir(self):
        return _nsstring_to_str(
            self.defaultManager.URLsForDirectory_inDomains_(
                NSMoviesDirectory, 1
            ).firstObject().absoluteString.UTF8String()
        )

    def _get_music_dir(self):
        return _nsstring_to_str(
            self.defaultManager.URLsForDirectory_inDomains_(
                NSMusicDirectory, 1
            ).firstObject().absoluteString.UTF8String()
        )

    def _get_pictures_dir(self):
        return _nsstring_to_str(
            self.defaultManager.URLsForDirectory_inDomains_(
                NSPicturesDirectory, 1
            ).firstObject().absoluteString.UTF8String()
        )

    def _get_application_dir(self):
        return _nsstring_to_str(
            self.defaultManager.URLsForDirectory_inDomains_(
                NSApplicationDirectory, 1
            ).firstObject().absoluteString.UTF8String()
        )

    def _get_desktop_dir(self):
        return _nsstring_to_str(
            self.defaultManager.URLsForDirectory_inDomains_(
                NSDesktopDirectory, 1
            ).firstObject().absoluteString.UTF8String()
        )


def instance():
    return OSXStoragePath()
