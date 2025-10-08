import subprocess as sb
from plyer.facades import Orientation


class LinuxOrientation(Orientation):

    def _set_landscape(self, **kwargs):
        self.rotate = 'inverted' if kwargs['reverse'] else 'normal'
        self.screen = sb.check_output(
            "xrandr -q | grep ' connected' |  head -n 1 | cut -d ' ' -f1",
            shell=True
        )
        self.screen = self.screen.decode('utf-8').split('\n')[0]
        sb.call(["xrandr", "--output", self.screen, "--rotate", self.rotate])

    def _set_portrait(self, **kwargs):
        self.rotate = 'right' if kwargs['reverse'] else 'left'
        self.screen = sb.check_output(
            "xrandr -q | grep ' connected' |  head -n 1 | cut -d ' ' -f1",
            shell=True
        )
        self.screen = self.screen.decode('utf-8').split('\n')[0]
        sb.call(["xrandr", "--output", self.screen, "--rotate", self.rotate])

    def _get_orientation(self, **kwargs):
        self.screen = sb.check_output(
            "xrandr -q | grep ' connected' |  head -n 1 | cut -d ' ' -f1",
            shell=True
        )
        self.screen = self.screen.decode('utf-8').split('\n')[0]

        try:
            orientation = sb.check_output(
                f"xrandr -q --verbose | grep {self.screen} | sed 's/primary //' | awk '{{print $5}}'",
                shell=True
            ).decode('utf-8').strip()
        except Exception:
            return 'unknown'

        orientations = {
            'normal': 'landscape',
            'inverted': 'landscape-reversed',
            'left': 'portrait',
            'right': 'portrait-reversed'
        }
        return orientations.get(orientation, 'unknown')


def instance():
    return LinuxOrientation()
