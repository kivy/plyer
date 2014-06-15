from AppKit import NSSound
from plyer.facades import PlaySound

class OSXPlaySound(PlaySound):
    def _load(self, filename):
        self.sound = NSSound.alloc()
        self.sound.initWithContentsOfFile_byReference_(filename, True)

    def _play(self):
    	print "PLaying"
        return self.sound.play()

def instance():
    return OSXPlaySound()
