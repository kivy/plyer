from jnius import autoclass
from plyer.facades import PlaySound

SoundPool = autoclass('android.media.SoundPool')
AudioManager = autoclass('android.media.AudioManager')

class AndroidPlaySound(PlaySound):
    def _load(self, filename):
        # Handles just one stream; first parameter
        self.soundpool = SoundPool(1, AudioManager.STREAM_MUSIC, 0);

        # Loads from file path, priority = 1
        self.soundID = self.soundpool.load(filename, 1);

    def _play(self):
        # int play (int soundID, float leftVolume, float rightVolume, int priority, int loop, float rate)
        ret = self.soundpool.play(self.soundID, 1.0, 1.0, 1, 0, 1.0);

        if (not ret):
            return False
        else:
            return True

def instance():
    return AndroidPlaySound()
