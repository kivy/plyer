from time import sleep
from jnius import autoclass
from plyer.facades import TTS
from . import activity

Locale = autoclass('java.util.Locale')
TextToSpeech = autoclass('android.speech.tts.TextToSpeech')


class AndroidTextToSpeech(TTS):
    def _speak(self, **kwargs):
        tts = TextToSpeech(activity, None)
        tts.setLanguage(Locale.US)  # TODO: locale specification as option
        retries = 0  # First try rarely succeeds due to some timing issue
        while retries < 100 and \
              tts.speak(kwargs.get('message').encode('utf-8'),
                        TextToSpeech.QUEUE_FLUSH, None) == -1:
            # -1 indicates error. Let's wait and then try again
            sleep(0.1)
            retries += 1


def instance():
    return AndroidTextToSpeech()
