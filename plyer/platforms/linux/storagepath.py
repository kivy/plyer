'''
Linux Storage Path
--------------------
'''

from plyer.facades import StoragePath
from os.path import expanduser, dirname, abspath

# Default paths for each name
USER_DIRS = "/.config/user-dirs.dirs"

PATHS = {
    "DESKTOP": "/Desktop",
    "DOCUMENTS": "/Documents",
    "DOWNLOAD": "/Downloads",
    "MUSIC": "/Music",
    "PICTURES": "/Pictures",
    "VIDEOS": "/Videos"
}


class LinuxStoragePath(StoragePath):

    def _get_from_user_dirs(self, name):
        try:
            with open(self._get_home_dir() + USER_DIRS, "r") as f:
                lines = f.readlines()
                # Find the line that starts with XDG_<name> to get the path
                index = [i for i, v in enumerate(lines)
                         if v.startswith("XDG_" + name)][0]
                return lines[index].split('"')[1]
        except KeyError:
            return PATHS[name]
        except Exception as e:
            raise e

    def _get_home_dir(self):
        return expanduser('~')

    def _get_external_storage_dir(self):
        return "/media/" + self._get_home_dir().split("/")[-1]

    def _get_root_dir(self):
        return "/"

    def _get_documents_dir(self):
        directory = self._get_from_user_dirs("DOCUMENT")
        return directory.replace("$HOME", self._get_home_dir())

    def _get_downloads_dir(self):
        directory = self._get_from_user_dirs("DOWNLOAD")
        return directory.replace("$HOME", self._get_home_dir())

    def _get_videos_dir(self):
        directory = self._get_from_user_dirs("VIDEOS")
        return directory.replace("$HOME", self._get_home_dir())

    def _get_music_dir(self):
        directory = self._get_from_user_dirs("MUSIC")
        return directory.replace("$HOME", self._get_home_dir())

    def _get_pictures_dir(self):
        directory = self._get_from_user_dirs("PICTURES")
        return directory.replace("$HOME", self._get_home_dir())

    def _get_application_dir(self):
        return dirname(abspath(__name__))


def instance():
    return LinuxStoragePath()
