import subprocess

from plyer.facades import TTS
from plyer.facades.tts import LanguageNotFound
from plyer.utils import whereis_exe


class EspeakTextToSpeech(TTS):
    '''Speaks using the espeak program
    '''

    def _language(self, **kwargs):
        ioreg_process = subprocess.Popen(["espeak",
                                          "--voices"], stdout=subprocess.PIPE)
        output = ioreg_process.communicate()[0]

        language = []
        if not output:
            return []

        for line in output.splitlines()[1:]:
            line_ws = line.split()
            language.append({'voice': line_ws[3], 'language': line_ws[1]})

        return language

    def _speak(self, **kwargs):
        ioreg_process = subprocess.Popen(
            ["espeak", kwargs.get('message'), "-v",
             kwargs.get('language')],
            stderr=subprocess.PIPE)
        output, error = ioreg_process.communicate()
        if error:
            raise LanguageNotFound(error)


def instance():
    if whereis_exe('espeak'):
        return EspeakTextToSpeech()
    return TTS()
