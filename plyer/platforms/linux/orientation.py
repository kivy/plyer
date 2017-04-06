from subprocess import call, check_output
from plyer.facades import Orientation
from plyer.utils import whereis_exe


class XrandrOrientation(Orientation):

    def _set_landscape(self, **kwargs):
        self.rotate = 'normal'
        self.screen = check_output("xrandr -q | grep ' connected' \
                              |  head -n 1 | cut -d ' ' -f1", shell=True)
        self.screen = self.screen.split('\n')[0]
        call(["xrandr", "--output", self.screen, "--rotate", self.rotate])

    def _set_portrait(self, **kwargs):
        self.rotate = 'left'
        self.screen = check_output("xrandr -q | grep ' connected' \
                              |  head -n 1 | cut -d ' ' -f1", shell=True)
        self.screen = self.screen.split('\n')[0]
        call(["xrandr", "--output", self.screen, "--rotate", self.rotate])


def instance():
    if whereis_exe('xrandr'):
        return XrandrOrientation()
    else:
        Orientation()
