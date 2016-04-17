import subprocess
from urllib import quote
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
from plyer.facades import Brightness
from plyer.utils import whereis_exe


class LinuxBrightness(Brightness):
    def _set_brightness(self, **kwargs):
        value = kwargs.get('value')
        time = kwargs.get('time')
        subprocess.Popen(["xbacklight", "-set", str(value), "-time",
                         str(time)])

    def _get_brightness(self, **kwargs):
        return subprocess.Popen(["xbacklight", "-get"])

    def _inc_brightness(self, **kwargs):
        increase_by = kwargs.get('increase_by')
        time = kwargs.get('time')
        subprocess.Popen(["xbacklight", "-inc", str(increase_by), "-time",
                         str(time)])

    def _dec_brightness(self, **kwargs):
        decrease_by = kwargs.get('decrease_by')
        time = kwargs.get('time')
        subprocess.Popen(["xbacklight", "-dec", str(decrease_by), "-time",
                         str(time)])


def instance():
    import sys
    if whereis_exe('xbacklight'):
        return LinuxBrightness()
    sys.stderr.write("xbacklight not found.")
    return Brightness()
