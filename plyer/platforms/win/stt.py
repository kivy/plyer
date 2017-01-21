# coding=utf-8

import speech_recognition as sr

from plyer.facades import STT


class WindowsSpeechToText(STT):
    """SpeechToText"""
    __language__ = {'af-ZA': 'Afrikaans (South Africa)',
                    'id-ID': 'Indonesian (Indonesia)',
                    'ms-MY': 'Malay (Malaysia)', 'ca-ES': 'Catalan (Spain)',
                    'cs-CZ': 'Czech (Czech Republic)',
                    'da-DK': 'Danish (Denmark)', 'de-DE': 'German (Germany)',
                    'en-AU': 'English (Australia)', 'en-CA': 'English (Canada)',
                    'en-GB': 'English (United Kingdom)',
                    'en-IN': 'English (India)', 'en-IE': 'English (Ireland)',
                    'en-NZ': 'English (New Zealand)',
                    'en-PH': 'English (Philippines)',
                    'en-ZA': 'English (South Africa)',
                    'en-US': 'English (United States)',
                    'es-AR': 'Spanish (Argentina)',
                    'es-BO': 'Spanish (Bolivia)', 'es-CL': 'Spanish (Chile)',
                    'es-CO': 'Spanish (Colombia)',
                    'es-CR': 'Spanish (Costa Rica)',
                    'es-EC': 'Spanish (Ecuador)',
                    'es-SV': 'Spanish (El Salvador)',
                    'es-ES': 'Spanish (Spain)',
                    'es-US': 'Spanish (United States)',
                    'es-GT': 'Spanish (Guatemala)',
                    'es-HN': 'Spanish (Honduras)', 'es-MX': 'Spanish (Mexico)',
                    'es-NI': 'Spanish (Nicaragua)', 'es-PA': 'Spanish (Panama)',
                    'es-PY': 'Spanish (Paraguay)', 'es-PE': 'Spanish (Peru)',
                    'es-PR': 'Spanish (Puerto Rico)',
                    'es-DO': 'Spanish (Dominican Republic)',
                    'es-UY': 'Spanish (Uruguay)',
                    'es-VE': 'Spanish (Venezuela)', 'eu-ES': 'Basque (Spain)',
                    'fil-PH': 'Filipino (Philippines)',
                    'fr-FR': 'French (France)', 'gl-ES': 'Galician (Spain)',
                    'hr-HR': 'Croatian (Croatia)',
                    'zu-ZA': 'Zulu (South Africa)',
                    'is-IS': 'Icelandic (Iceland)', 'it-IT': 'Italian (Italy)',
                    'lt-LT': 'Lithuanian (Lithuania)',
                    'hu-HU': 'Hungarian (Hungary)',
                    'nl-NL': 'Dutch (Netherlands)',
                    'nb-NO': 'Norwegian Bokmål (Norway)',
                    'pl-PL': 'Polish (Poland)', 'pt-BR': 'Portuguese (Brazil)',
                    'pt-PT': 'Portuguese (Portugal)',
                    'ro-RO': 'Romanian (Romania)', 'sk-SK': 'Slovak (Slovakia)',
                    'sl-SI': 'Slovenian (Slovenia)',
                    'fi-FI': 'Finnish (Finland)', 'sv-SE': 'Swedish (Sweden)',
                    'vi-VN': 'Vietnamese (Vietnam)',
                    'tr-TR': 'Turkish (Turkey)', 'el-GR': 'Greek (Greece)',
                    'bg-BG': 'Bulgarian (Bulgaria)',
                    'ru-RU': 'Russian (Russia)', 'sr-RS': 'Serbian (Serbia)',
                    'uk-UA': 'Ukrainian (Ukraine)', 'he-IL': 'Hebrew (Israel)',
                    'ar-IL': 'Arabic (Israel)', 'ar-JO': 'Arabic (Jordan)',
                    'ar-AE': 'Arabic (United Arab Emirates)',
                    'ar-BH': 'Arabic (Bahrain)', 'ar-DZ': 'Arabic (Algeria)',
                    'ar-SA': 'Arabic (Saudi Arabia)', 'ar-IQ': 'Arabic (Iraq)',
                    'ar-KW': 'Arabic (Kuwait)', 'ar-MA': 'Arabic (Morocco)',
                    'ar-TN': 'Arabic (Tunisia)', 'ar-OM': 'Arabic (Oman)',
                    'ar-PS': 'Arabic (State of Palestine)',
                    'ar-QA': 'Arabic (Qatar)', 'ar-LB': 'Arabic (Lebanon)',
                    'ar-EG': 'Arabic (Egypt)', 'fa-IR': 'Persian (Iran)',
                    'hi-IN': 'Hindi (India)', 'th-TH': 'Thai (Thailand)',
                    }
    recognizer = sr.Recognizer()

    def _recognize_microphone(self, language, filename):
        """Recognize speech using CMUSphinx

        The Google Speech Recognition API key is specified by ``key``.
        If not specified, it uses a generic key that works out of the box.
        This should generally be used for personal or testing purposes only,
        as it **may be revoked by Google at any time**.

        To obtain your own API key, simply following the steps on the `API Keys
         <http://www.chromium.org/developers/how-tos/api-keys>`__ page at the
         Chromium Developers site. In the Google Developers Console,
         Google Speech Recognition is listed as "Speech API".

         Raises a ``ValueError`` exception if the
         speech is unintelligible. Raises a ``IOError``
         exception if the speech recognition operation failed, if the key isn't
         valid, or if there is no internet connection.
         """
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            print audio
        if filename:
            if not filename.endswith('.wav'):
                filename += '.wav'

            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())

        try:
            return self.recognizer.recognize_sphinx(audio)
        except sr.UnknownValueError:
            raise STT.UnknownValueError
        except sr.RequestError as e:
            raise STT.RequestError(e)

    def _callibrate(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def _listen_in_background(self, callback, language):
        def background_callback(recognizer, audio):
            try:
                transcribe_text = recognizer.recognize_sphinx(
                    audio, language=language)
                callback(transcribe_text)
            except sr.UnknownValueError:
                raise STT.UnknownValueError
            except sr.RequestError as e:
                raise STT.RequestError(e)

        return self.recognizer.listen_in_background(
            sr.Microphone(), background_callback)

    def _transcribe_audio(self, filename, language):
        """
        WAV files must be in PCM/LPCM format; WAVE_FORMAT_EXTENSIBLE and
        compressed WAV are not supported and may result in undefined behaviour.

        Both AIFF and AIFF-C (compressed AIFF) formats are supported.

        FLAC files must be in native FLAC format; OGG-FLAC is not supported and
        may result in undefined behaviour.
        """
        with sr.AudioFile(filename) as source:
            audio = self.recognizer.record(source)

        try:
            return self.recognizer.recognize_sphinx(audio, language=language)
        except sr.UnknownValueError:
            raise STT.UnknownValueError
        except sr.RequestError as e:
            raise STT.RequestError(e)

    def _language(self):
        return self.__language__


def instance():
    return WindowsSpeechToText()
