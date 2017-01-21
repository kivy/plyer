"""
STT
====

The :class:`STT` provides provides access to public methods to
use speech to text of your device.

Simple Examples
---------------

To ask speech recognition engine to begin listening for single command::
    >>> from plyer import stt
    >>> print stt.recognize_microphone()

To get language::
    >>> from plyer import stt
    >>> stt.language()

To get callibrate::
    >>> from plyer import stt
    >>> stt.language()

To ask speech recognition engine to begin listening for multiple command::
    >>> from __future__ import print_function
    >>> from plyer import stt
    >>> import time
    >>> stop_listening = stt.listen_in_background(lambda text: print(text))
    >>> time.sleep(10)
    >>> stop_listening()

To ask speech recognition engine to Transcribe Audio::
    >>> from plyer import stt
    >>> print stt.recognize_microphone('audio.wav')
"""


class STT(object):
    class RequestError(Exception):
        pass

    class UnknownValueError(Exception):
        pass

    """SpeechToText Facade."""

    def recognize_microphone(self, language='en-US', filename=None):
        """Tells the speech recognition engine to begin listening."""

        return self._recognize_microphone(language, filename)

    def transcribe_audio(self, filename, language='en-US'):
        """
        """
        self._transcribe_audio(filename, language)

    def callibrate(self):
        """Calibrate the energy threshold for ambient noise levels"""
        self._callibrate()

    def listen_in_background(self, callback, language='en-US'):
        """Tells the speech recognition engine to begin
        listening in background"""
        return self._listen_in_background(callback, language)

    def language(self):
        """Return all language supported"""
        return self._language()

    # private

    def _recognize_microphone(self, language, filename):
        """"""
        raise NotImplementedError()

    def _transcribe_audio(self, filename, language):
        """"""
        raise NotImplementedError()

    def _callibrate(self):
        """"""
        raise NotImplementedError()

    def _listen_in_background(self, callback, language):
        """"""
        raise NotImplementedError()

    def _language(self):
        """"""
        raise NotImplementedError()
