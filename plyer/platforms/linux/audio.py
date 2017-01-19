from __future__ import print_function
import select
import sys
import wave
import pyaudio
from plyer.facades.audio import Audio

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 600
WAVE_OUTPUT_FILENAME = "recording.wav"

record_audio = pyaudio.PyAudio()

play_audio = pyaudio.PyAudio()


r_stream = record_audio.open(format=FORMAT, channels=CHANNELS,
                             rate=RATE, input=True,
                             frames_per_buffer=CHUNK)

frames = []


if sys.version_info.major == 3:
    def raw_input(*args, **kwargs):
        return input(*args, **kwargs)


class LinuxAudio(Audio):
    def __init__(self, file_path=None):
        default_path = '/home/recording.wav'
        super(LinuxAudio, self).__init__(file_path or default_path)

    def _start(self):

        print("recording started ... press Enter to stop recording")

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = r_stream.read(CHUNK)
            frames.append(data)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                raw_input()  # Wait for stop
                self._stop()
                break

    def _stop(self):
        r_stream.stop_stream()
        r_stream.close()
        record_audio.terminate()
        wave_file = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(record_audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
        print("recording stopped")

    def _play(self):
        wf = wave.open("recording.wav", 'rb')
        audio_format = play_audio.get_format_from_width(wf.getsampwidth())
        p_stream = play_audio.open(format=audio_format,
                                   channels=wf.getnchannels(),
                                   rate=wf.getframerate(),
                                   output=True)
        data = wf.readframes(CHUNK)
        while data != '':
            p_stream.write(data)
            data = wf.readframes(CHUNK)
        p_stream.stop_stream()
        p_stream.close()
        play_audio.terminate()


def instance():
    return LinuxAudio()
