'''Linun Speech Recognition'''

import multiprocessing
import speech_recognition as sr

from plyer.facades import Speech


class LinuxSpeech(Speech):

    _process = None
    _audio = None

    def _on_start(self):
        print 'starting thread'
        self._recognizer.energy_threshold = 2000
        # with sr.Microphone() as source:
        #     self._recognizer.adjust_for_ambient_noise(source, duration=1)
        #     self._audio = self._recognizer.listen(source, timeout=3)
        self._recognizer.listen_in_background(sr.Microphone(), self._on_results)
        # self.stop()

    def _on_results(self, rec, audio):
        print 'mamy audio'
        print rec.recognize(audio, show_all=True)
        self._audio = audio
        self.stop()

    def _exist(self):
        return bool(sr.Microphone() and self._recognizer)

    def _stop(self):
        if self._process is not None:
            self._process.terminate()

        if not isinstance(self._audio, sr.AudioData):
            return

        try:
            results = self._recognizer.recognize(self._audio, show_all=True)
            self.results = [res['text'] for res in results]
        except IndexError:
            self.results.append('ERROR:internet_connection')
        except LookupError:
            self.results.append('ERROR:no_match')

    def _start(self):

        self._recognizer.energy_threshold = 2000
        self._process = multiprocessing.Process(target=self._on_start)
        self._process.start()

        # with sr.Microphone() as source:
        #     self._recognizer.adjust_for_ambient_noise(source, duration=1)
        #     self._audio = self._recognizer.listen(source, timeout=3)
        # self._recognizer.listen_in_background(sr.Microphone(),
        # self._on_results)
        # self.stop()

    def __init__(self):
        super(Speech, self).__init__()
        self._recognizer = sr.Recognizer(self.language)


def instance():
    return LinuxSpeech()
