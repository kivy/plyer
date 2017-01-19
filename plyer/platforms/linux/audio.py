import pyaudio
import wave
import sys
import select
import os
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


class LinuxAudio(Audio):

    def __init__(self, file_path=None):
        default_path = '/home/recording.wav'
        super(LinuxAudio, self).__init__(file_path or default_path)

    def _start(self):

        print "recording started ... press Enter to stop recording"

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = r_stream.read(CHUNK)
            frames.append(data)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = raw_input()
                self._stop()
                break

    def _stop(self):
        r_stream.stop_stream()
        r_stream.close()
        record_audio.terminate()
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(record_audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        print "recording stopped"

    def _play(self):
        wf = wave.open("recording.wav", 'rb')
        p_stream = play_audio.open(
                     format=play_audio.get_format_from_width(wf.getsampwidth()),
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
