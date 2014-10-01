'''
Kivy-based camera implementation
--------------------------------
'''

from os import unlink, path
from plyer.facades import Camera
from subprocess import Popen
from tempfile import mktemp
from threading import Thread

# Taken from http://stackoverflow.com/a/10823905/1124621
def popenAndCall(onExit, *popenArgs, **popenKWArgs):
    """
    Runs a subprocess.Popen, and then calls the function onExit when the
    subprocess completes.

    Use it exactly the way you'd normally use subprocess.Popen, except include a
    callable to execute as the first argument. onExit is a callable object, and
    *popenArgs and **popenKWArgs are simply passed up to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs, popenKWArgs):
        proc = Popen(*popenArgs, **popenKWArgs)
        proc.wait()
        onExit()
        return

    thread = Thread(target=runInThread,
                    args=(onExit, popenArgs, popenKWArgs))
    thread.start()

    return thread # returns immediately after the thread starts


class KivyCamera(Camera):
    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        if self.filename == None:
            self.filename = mktemp() + ".jpg"

        popenAndCall(self._callback, ["kivy-camera", "-o", "-O", self.filename])
        return

    def _callback(self):
        if self.on_complete(self.filename):
            self._unlink(self.filename)

    def _unlink(self, fn):
        try:
            unlink(fn)
        except:
            pass


def instance():
    return KivyCamera()
