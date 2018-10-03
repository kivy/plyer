'''
TTS
====

The :class:`TTS` provides provides access to public methods to
use text to speech of your device.

Simple Examples
---------------

To speak::

    >>> from plyer import tts
    >>> tts.speak(message=message)

Supported Platforms
-------------------
Android, iOS, Windows, OS X, Linux

'''


class TTS(object):
    '''
    TextToSpeech facade.
    '''

    def speak(self, message=''):
        '''Use text to speech capabilities to speak the message.

        :param message: What to speak
        :type message: str
        '''
        self._speak(message=message)

    def speak_to_file(self,message='',fileName=''):
        '''Use text to speech capabilities to speak message into file(mp3,wav,ogg)

        :param message: What to speak
        :type message: str
        :type fileName: str
        '''
        
        self._speak_to_file(message=message,fileName=fileName)
    



    # private




    def _speak(self, **kwargs):
        raise NotImplementedError()
    
    def _speak_to_file(self, **kwargs):
        raise NotImplementedError()
