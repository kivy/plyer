import subprocess
from plyer.facades import TextToSpeech
from plyer.utils import whereis_exe


class NativeSayTextToSpeech(TextToSpeech):
    '''Speaks using the native OSX 'say' command
    '''
    def _speak(self, **kwargs):
        subprocess.call(["say", kwargs.get('message')])


class EspeakTextToSpeech(TextToSpeech):
    '''Speaks using the espeak program
    '''
    def _speak(self, **kwargs):
        subprocess.call(["espeak", kwargs.get('message')])


def instance():
    if whereis_exe('say'):
        return NativeSayTextToSpeech()
    elif whereis_exe('espeak'):
        return EspeakTextToSpeech()
    raise NotImplemented()
