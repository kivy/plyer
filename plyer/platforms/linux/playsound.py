import subprocess
from plyer.facades import PlaySound

class LinuxPlaySound(PlaySound):
    def _load(self, filename):
        self.filename = filename

    def _play(self):
        if (not self.filename):
            return False
        
        try:
            subprocess.Popen(["play", self.filename])
            return True
        except OSError:
            try:
                subprocess.Popen(["aplay", self.filename])
                return True
            except OSError:
                return False

def instance():
    return LinuxPlaySound()
