from plyer.facades.audio import Audio
import subprocess


class LinuxAudio(Audio):
    def __init__(self, file_path=None):
        default_path = 'test.mp3'
        super(LinuxAudio, self).__init__(file_path or default_path)

    def _start(self):
        self.process = subprocess.Popen(["gst-launch-1.0", "autoaudiosrc",
                                    "num-buffers=100", "!", "audioconvert",
                                    "!", "vorbisenc", "!", "oggmux", "!",
                                    "filesink", "location=" + self.file_path])
        self.process.wait()

    def _stop(self):
        self.process.terminate()

    def _play(self):
        self.file_path = str(self.file_path)
        subprocess.call(["gst-launch-1.0", "filesrc",
                         "location=" + self.file_path, "!", "decodebin",
                         "!", "pulsesink"])


def instance():
    return LinuxAudio()
