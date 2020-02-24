'''
TTS
====

The :class:`TTS` provides provides access to public methods to
use text to speech of your device.

Simple Examples
---------------

To speak::

    >>> from plyer import tts
    >>> tts.speak(message='Put message here', language='')

To get language::

    >>> from plyer import tts
    >>> tts.language()

Supported Platforms
-------------------
Android, iOS, Windows, OS X, Linux

'''


class LanguageNotFound(Exception):
    """Raise when a specific language not found"""

    def __init__(self, message):
        self.message = message
        super(LanguageNotFound, self).__init__(message)


class TTS(object):
    """TextToSpeech facade."""

    def speak(self, message='', language=''):
        """Use text to speech capabilities to speak the message.

        :param message: What to speak
        :type message: str

        :param language: In which language to speak
        :type language: str
        """
        self._speak(message=message, language=language)

    def language(self):
        """Get all the language for text to speech capabilities

        :rtype: language: List of language in which can speak
        """
        return self._language()

    # private

    def _speak(self, **kwargs):
        raise NotImplementedError()

    def _language(self, **kwargs):
        raise NotImplementedError()
