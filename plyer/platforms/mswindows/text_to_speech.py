import subprocess
from plyer.facades import TextToSpeech
from plyer.utils import whereis_exe


class EspeakTextToSpeech(TextToSpeech):
    ''' Speaks using the espeak program
    '''
    def _speak(self, **kwargs):
        subprocess.call(["espeak", kwargs.get('message')])


def instance():
    if whereis_exe('espeak'):
        return WindowsTextToSpeech()
    raise NotImplemented()
