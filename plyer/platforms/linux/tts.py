import subprocess
from plyer.facades import TTS
from plyer.utils import whereis_exe


class EspeakTextToSpeech(TTS):
    ''' Speaks using the espeak program
    '''
    def _speak(self, **kwargs):
        subprocess.call(["espeak", kwargs.get('message')])


    def _speak_to_file(self,**kwargs):
        '''save the text message into file(mp3, ogg,wav) '''
            
        subprocess.call(["espeak", kwargs.get('message'), \
                        "-w" ,kwargs.get('fileName')])

class FliteTextToSpeech(TTS):
    ''' Speaks using the flite program
    '''
    def _speak(self):
        subprocess.call(["flite", "-t", kwargs.get('message'), "play"])


def instance():
    if whereis_exe('espeak'):
        return EspeakTextToSpeech()
    elif whereis_exe('flite'):
        return FlitetextToSpeech()
    return TTS()
