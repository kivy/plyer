import winsound
from plyer.facades import PlaySound

class WinPlaySound(PlaySound):
    def _load(self, filename):
        self.filename = filename

    def _play(self):
        return winsound.PlaySound(self.filename, winsound.SND_FILENAME)

def instance():
    return WinPlaySound()
