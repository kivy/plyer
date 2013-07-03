import subprocess
from plyer.facades import TextToSpeech
from plyer.utils import whereis_exe


class EspeakTextToSpeech(TextToSpeech):
    ''' Speaks using the espeak program
    '''
    def _speak(self, **kwargs):
        subprocess.call(["espeak", kwargs.get('message')])


class FliteTextToSpeech(TextToSpeech):
    ''' Speaks using the flite program
    '''
    def _speak(self):
        subprocess.call(["flite", "-t", kwargs.get('message'), "play"])


def instance():
    if whereis_exe('espeak'):
        return EspeakTextToSpeech()
    elif whereis_exe('flite'):
        return FlitetextToSpeech()
    raise NotImplemented()
