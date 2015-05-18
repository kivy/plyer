'''Linun Speech Recognition'''

from multiprocessing import Process, Manager, Queue
import speech_recognition as sr

from plyer.facades import Speech

class SpeechListener(Process):

    def __init__(self, queue, recognizer):
        super(SpeechListener, self).__init__()
        self.queue = queue
        self.recognizer = recognizer

    def run(self):

        # self._recognizer.listen_in_background(sr.Microphone(), self._on_results)
        # with sr.Microphone() as source:
        #     self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print 'starting listen'
        # self.recognizer.energy_threshold = 4000
        # self.recognizer.listen_in_background(sr.Microphone(), self.on_result)
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self._audio = self.recognizer.listen(source)
            print 'after listen'
        try:
            results = self.recognizer.recognize(self._audio, show_all=True)
            self.queue.put(results)
            # self.r = {i : res['text'] for i, res in enumerate(results)}
            v = len(results)
            print 'results', v
        except IndexError:
            pass
            # self.results.append('ERROR:internet_connection')
        except LookupError:
            pass
            # self.results.append('ERROR:no_match')

    def on_result(self, recognizer, audio):
        print 'have some results'
        try:
            results = recognizer.recognize(audio, show_all=True)
            self.queue.put(results)
            # self.r = {i : res['text'] for i, res in enumerate(results)}
            v = len(results)
            print 'results', v
        # except IndexError:
        #     pass
            # self.results.append('ERROR:internet_connection')
        except LookupError:
            pass
            print 'ERROR'



class LinuxSpeech(Speech):

    _process = None
    _audio = None

    def _on_start(self, recognizer, v, q):
        print 'starting thread', v, self.r, q, q.get()

        q.put('asdf')
        recognizer.energy_threshold = 2000
        # with sr.Microphone() as source:
        #     recognizer.adjust_for_ambient_noise(source, duration=1)
        #     print 'starting listen'
        #     self._audio = recognizer.listen(source)
        #     print 'after listen'
        # try:
        #     results = recognizer.recognize(self._audio, show_all=True)
        #     # self.r = {i : res['text'] for i, res in enumerate(results)}
        #     v = len(results)
        #     print 'results', v
        # except IndexError:
        #     pass
        #     # self.results.append('ERROR:internet_connection')
        # except LookupError:
        #     pass
        # #     self.results.append('ERROR:no_match')

        recognizer.listen_in_background(sr.Microphone(), self._on_results)
        print 'stopping', v
        # self.stop()

    def get_results(self):
        pass

    def _on_results(self, rec, audio):
        print 'mamy audio'
        print 'queue:', self._queue.get()
        # self._audio = audio
        # self.stop()

    def _stop(self):
        # self._process.join()
        print 'c', self._queue.get(0)
        # print 'results r', self.r
        try:
            if self._process is not None and self._process.is_alive():
                self._process.terminate()
        except AttributeError:
            print 'artrt'
        #
        # print self._audio, self._audio.__class__
        # if not isinstance(self._audio, sr.AudioData):
        #     return
        #
        # try:
        #     results = self._recognizer.recognize(self._audio, show_all=True)
        #     self.results = [res['text'] for res in results]
        #     print 'results', self.results
        # except IndexError:
        #     self.results.append('ERROR:internet_connection')
        # except LookupError:
        #     self.results.append('ERROR:no_match')

    def _start(self):
        self._queue = Queue()
        self._process = SpeechListener(self._queue, self._recognizer)
        self._process.start()

        # self.queue.put(50)
        # self._audio = None
        # self.r = Manager().Value('i', 0)
        # self.r = 99
        # self._recognizer.energy_threshold = 2000
        # self._process = Process(target=self._on_start, args=(self._recognizer, self.r,self.queue))
        # self._process.start()
        # self._process.join()
        #
        # with sr.Microphone() as source:
        #     self._recognizer.adjust_for_ambient_noise(source, duration=1)
        #     self._audio = self._recognizer.listen(source)
        # self._recognizer.listen(
        #     sr.Microphone(),
        #     self._on_results
        # )
        # self.stop()

    def _exist(self):
        return bool(sr.Microphone() and self._recognizer)

    def __init__(self):
        super(Speech, self).__init__()
        self._recognizer = sr.Recognizer(self.language)


def instance():
    return LinuxSpeech()
