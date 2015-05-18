from android.runnable import run_on_ui_thread

from jnius import autoclass
from jnius import java_method
from jnius import PythonJavaClass

from plyer.facades import Speech
from plyer.platforms.android import activity

ArrayList = autoclass('java.util.ArrayList')
Bundle = autoclass('android.os.Bundle')
Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')
RecognizerIntent = autoclass('android.speech.RecognizerIntent')
RecognitionListener = autoclass('android.speech.RecognitionListener')
SpeechRecognizer = autoclass('android.speech.SpeechRecognizer')

SpeechResults = SpeechRecognizer.RESULTS_RECOGNITION


class SpeechListener(PythonJavaClass):
    __javainterfaces__ = ['android/speech/RecognitionListener']

    def __init__(self):
        super(SpeechListener, self).__init__()
        self.error_callback = None
        self.result_callback = None
        self.volume_callback = None

    def set_error_callback(self, callback):
        '''Set error callback. It is called when error occurs.

        :param callback: function with one param of error message.
        '''
        self.error_callback = callback

    def set_result_callback(self, callback):
        '''Set result callback. It is called when result are receiver.

        :param callback: function with one param of lists of results
            where elements are strings of texts.
        '''
        self.result_callback = callback

    def set_volume_changed_callback(self, callback):
        '''Set volume voice callback.

        It is called when loudness of voice changes.

        :param callback: function with one param of volume
            in range from 0.0 to 1.0.
        :return:
        '''
        self.volume_callback = callback

    # Implementation Java Interfaces

    @java_method('()V')
    def onBeginningOfSpeech(self):
        pass

    @java_method('([B)V')
    def onBufferReceived(self, buffer):
        pass

    @java_method('()V')
    def onEndOfSpeech(self):
        pass

    @java_method('(I)V')
    def onError(self, error):
        msg = ''
        if error == SpeechRecognizer.ERROR_AUDIO:
            msg = 'audio'
        if error == SpeechRecognizer.ERROR_CLIENT:
            msg = 'client'
        if error == SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS:
            msg = 'insufficient_permissions'
        if error == SpeechRecognizer.ERROR_NETWORK:
            msg = 'network'
        if error == SpeechRecognizer.ERROR_NETWORK_TIMEOUT:
            msg = 'network_timeout'
        if error == SpeechRecognizer.ERROR_NO_MATCH:
            msg = 'no_match'
        if error == SpeechRecognizer.ERROR_RECOGNIZER_BUSY:
            msg = 'recognizer_busy'
        if error == SpeechRecognizer.ERROR_SERVER:
            msg = 'server'
        if error == SpeechRecognizer.ERROR_SPEECH_TIMEOUT:
            msg = 'speech_timeout'

        if msg and self.error_callback:
            self.error_callback('error:' + msg)

    @java_method('(ILandroid/os/Bundle;)V')
    def onEvent(self, event_type, params):
        pass

    @java_method('(Landroid/os/Bundle;)V')
    def onPartialResults(self):
        pass

    @java_method('(Landroid/os/Bundle;)V')
    def onReadyForSpeech(self, params):
        pass

    @java_method('(Landroid/os/Bundle;)V')
    def onResults(self, results):
        texts = []
        matches = results.getStringArrayList(SpeechResults)
        for match in matches.toArray():
            texts.append(match.decode('ascii', 'ignore'))

        if texts and self.result_callback:
            self.result_callback(texts)

    @java_method('(F)V')
    def onRmsChanged(self, rmsdB):
        if self.set_volume_changed_callback:
            self.set_volume_changed_callback(rmsdB)


class AndroidSpeech(Speech):
    '''Android Speech Implementation.

    Works on API >= 9.
    Android class `SpeechRecognizer` deactivates automatically.

    Class methods `_on_error()`, `_on_result()` are some kind of listeners.
    Android on finish listening sends one of result: error or possible matches
    '''

    def _on_error(self, msg):
        self.results.append(msg)
        self.stop()

    def _on_result(self, messages):
        self.results.extend(messages)
        self.stop()

    @run_on_ui_thread
    def _start(self):
        intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE,
                        self.language)
        intent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE,
                        activity.getPackageName())
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                        RecognizerIntent.LANGUAGE_MODEL_WEB_SEARCH)
        intent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1000)

        listener = SpeechListener()
        listener.set_error_callback(self._on_error)
        listener.set_result_callback(self._on_result)

        self.speech = SpeechRecognizer.createSpeechRecognizer(activity)
        self.speech.setRecognitionListener(listener)
        self.speech.startListening(intent)

    def _stop(self):
        if self.speech:
            self.speech.stopListening()
        self.speech = None

    def _exist(self):
        return bool(SpeechRecognizer.isRecognitionAvailable(activity))


def instance():
    return AndroidSpeech()
