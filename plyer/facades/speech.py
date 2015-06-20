class Speech(object):
    '''Speech Recognition facade.

    In order to check that your device supports voice recognition use method
    `exist`.

    Variable `language` indicates which language will be used to match words
    from voice.

    Use `start` to start voice recognition immediately and `stop` to stop.

    .. note::
        Needed permissions for Android: RECORD_AUDIO and NETWORK.
        Network are needed when voice recognition wanted to be checked online.

    .. note::
        On Android platform, after execute `start` method you can hear BEEP!
        Mute sound in order to disable it.
    '''

    _language = 'en-US'
    '''default language in which platform will try to recognize voice.
    In order to change language pick one from list by using
    `supported_languages` method.
    '''

    _supported_languages = [
        'en-US',
        'pl-PL'
    ]

    results = []
    '''List of sentences found while listening. It may consist of many similar
    and possible sentences that was recognition program.'''

    state = None
    '''Current state of class. It may become `listening` and `ready`.'''

    @property
    def supported_languages(self):
        '''Return list of supported languages used in recognition.'''
        return self._supported_languages

    @property
    def language(self):
        '''Return current language.'''
        return self._language

    @language.setter
    def language(self, lang):
        '''Set current language.

        Value can not be set if it's not supported. See `supported_languages`
        to get what language you can set.
        '''
        if lang in self.supported_languages:
            self._language = lang

    # Public Methods
    def start(self):
        '''Start listening.'''
        self.results = []
        self._start()
        self.state = 'listening'

    def stop(self):
        '''Stop listening.'''
        self._stop()
        self.state = 'ready'

    def exist(self):
        '''True if Speech Recognition is available.'''
        return self._exist()

    # Private Methods
    def _start(self):
        raise NotImplementedError

    def _stop(self):
        raise NotImplementedError

    def _exist(self):
        raise NotImplementedError
