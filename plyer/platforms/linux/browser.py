import subprocess
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
from plyer.facades import Browser
from plyer.utils import whereis_exe


class LinuxBrowser(Browser):
    def _open(self, **kwargs):
        uri = kwargs.get('uri')
        subprocess.Popen(["xdg-open", uri])


def instance():
    import sys
    if whereis_exe('xdg-open'):
        return LinuxBrowser()
    sys.stderr.write("xdg-open not found.")
    return Browser()
