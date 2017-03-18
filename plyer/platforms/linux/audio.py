from plyer.facades.audio import Audio
import subprocess


class LinuxAudio(Audio):
    def __init__(self, file_path=None):
        default_path = '/home/recording.wav'
        super(LinuxAudio, self).__init__(file_path or default_path)

    def _start(self):
        process = subprocess.Popen(("gst-launch", "autoaudiosrc",
                                    "num-buffers=100", "!", "audioconvert",
                                    "!", "vorbisenc", "!", "oggmux", "!",
                                    "filesink", "location=" + self.file_path),
                                   stdout=subprocess.PIPE)
        process.wait()

    def _stop(self):
        process.terminate()

    def _play(self):
        subprocess.call(["gst-launch", "filesrc",
                         "location=" + self.file_path, "!", "decodebin",
                         "audioconvert", "!", "pulsesink"])


def instance():
    return LinuxAudio()
