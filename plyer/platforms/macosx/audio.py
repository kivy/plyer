from plyer.facades.audio import Audio
import subprocess
from plyer.utils import whereis_exe


class SnapAudio(Audio):
    def __init__(self, file_path=None):
        default_path = '/home/recording.wav'
        super(SnapAudio, self).__init__(file_path or default_path)
        self.filename = str(file_path)
        
    def _start(self):
        process = subprocess.Popen(("videosnap", "-w", 2, filename),
                                   stdout=subprocess.PIPE)
        process.wait()

    def _stop(self):
        process.terminate()

    def _play(self):
        subprocess.call(["afplay", filename, "&"])
        

class SOXAudio(Audio):
    def __init__(self, file_path=None):
        default_path = '/home/recording.wav'
        super(SOXAudio, self).__init__(file_path or default_path)
        self.filename = str(file_path)
        
    def _start(self):
        process = subprocess.Popen(("sox", "-d", filename),
                                   stdout=subprocess.PIPE)
        process.wait()

    def _stop(self):
        process.terminate()

    def _play(self):
        subprocess.call(["afplay", filename, "&"])


def instance():
    if whereis_exe('videosnap'):
        return SnapAudio()
     elif whereis_exe('sox'):
         return SOXAudio()
    return Audio()
