from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing.queues import Empty
import pyaudio
import wave
import time
from plyer.facades.audio import Audio

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

SIGNAL = {
    'start_playing': 1,
    'stop_playing': 2,
    'start_recording': 3,
    'stop_recording': 4,
}


class AudioWorker(Process):
    '''Process for recording and playing audio files.

    Rather wave files.
    AudioWorker is separated process. On start listens on queue for first
    signal. That signal tells about what job he should do - recording
    or playing. On another signal we stops worker.
    '''

    audio = None
    stream = None
    frames = None

    def __init__(self, file_path, queue, *args, **kwargs):
        super(AudioWorker, self).__init__(*args, **kwargs)
        self.file_path = file_path
        self.queue = queue

    def get_signal(self):
        try:
            signal = self.queue.get(0)
            return signal
        except Empty:
            pass

    def run(self):
        super(AudioWorker, self).run()
        signal = None
        while not signal:
            signal = self.get_signal()
            time.sleep(1 / 100)

        if signal == SIGNAL['start_recording']:
            self.start_recording()
        elif signal == SIGNAL['start_playing']:
            self.start_playing()
        else:
            self.terminate()

    def start_recording(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        self.frames = []

        while self.get_signal() != SIGNAL['stop_recording']:
            data = self.stream.read(CHUNK)
            self.frames.append(data)

        self.stop_recording()

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        wave_file = wave.open(self.file_path, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()

    def start_playing(self):
        self.audio = pyaudio.PyAudio()
        wave_file = wave.open(self.file_path, 'rb')
        self.stream = self.audio.open(
            format=self.audio.get_format_from_width(wave_file.getsampwidth()),
            channels=wave_file.getnchannels(),
            rate=wave_file.getframerate(),
            output=True
        )
        # read data
        data = wave_file.readframes(CHUNK)

        while data != '' and self.get_signal() != SIGNAL['stop_playing']:
            self.stream.write(data)
            data = wave_file.readframes(CHUNK)

        self.stop_playing()

    def stop_playing(self):
        # stop stream
        self.stream.stop_stream()
        self.stream.close()

        # close PyAudio
        self.audio.terminate()


class LinuxAudio(Audio):

    _process = None
    '''Process for recording and playing audio.'''

    _queue = None
    '''Queue for communication with our process.'''

    def _on_start(self):
        pass

    def __init__(self, file_path=None):
        default_path = 'testrecorder.waw'
        super(LinuxAudio, self).__init__(file_path or default_path)

        self._queue = Queue()

    def _start(self):
        self._process = AudioWorker(self._file_path, self._queue)
        self._queue.put(SIGNAL['start_recording'])
        self._process.start()

    def _stop(self):
        if self.state == 'recording':
            self._queue.put(SIGNAL['stop_recording'])
        if self.state == 'playing':
            self._queue.put(SIGNAL['stop_playing'])
        self._process.join()
        self._process.terminate()

    def _play(self):
        self._process = AudioWorker(self._file_path, self._queue)
        self._queue.put(SIGNAL['start_playing'])
        self._process.start()


def instance():
    return LinuxAudio()
