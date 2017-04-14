from subprocess import call, Popen, PIPE
from plyer.facades import Orientation
from plyer.utils import whereis_exe


class XrandrOrientation(Orientation):

    def _set_landscape(self, **kwargs):
        self.rotate = 'normal'
        xrandr_process = Popen(["xrandr", "-q"], stdout=PIPE, stderr=PIPE)
        grep_process_one = Popen(["grep", "connected"],
            stdin=xrandr_process.stdout, stdout=PIPE)
        grep_process_two = Popen(["head", "-n", "1"],
            stdin=grep_process_one.stdout, stdout=PIPE)
        grep_process_three = Popen(["cut", "-d", " ", "-f1"],
            stdin=grep_process_two.stdout, stdout=PIPE)
        xrandr_process.stdout.close()
        output = grep_process_three.communicate()[0]
        output = output.split()[0]
        call(["xrandr", "--output", output, "--rotate", self.rotate])

    def _set_portrait(self, **kwargs):
        self.rotate = 'left'
        xrandr_process = Popen(["xrandr", "-q"], stdout=PIPE, stderr=PIPE)
        grep_process_one = Popen(["grep", "connected"],
            stdin=xrandr_process.stdout, stdout=PIPE)
        grep_process_two = Popen(["head", "-n", "1"],
            stdin=grep_process_one.stdout, stdout=PIPE)
        grep_process_three = Popen(["cut", "-d", " ", "-f1"],
            stdin=grep_process_two.stdout, stdout=PIPE)
        xrandr_process.stdout.close()
        output = grep_process_three.communicate()[0]
        output = output.split()[0]
        call(["xrandr", "--output", output, "--rotate", self.rotate])


def instance():
    if whereis_exe('xrandr'):
        return XrandrOrientation()
    else:
        return Orientation()
