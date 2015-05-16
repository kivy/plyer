class Speech(object):
    '''Speech Recognition facade.

    In order to check that your device supports voice recognition use method
    `exist`.

    Variable `language` indicate which language will be used to match words
    from voice.

    Try `start` to start voice recognition immediately and `stop` to stop.

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
    '''List of strings found while listening.'''

    errors = []
    '''List of errors occured while listening.'''

    state = None

    @property
    def supported_languages(self):
        return self._supported_languages

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, lang):
        if lang in self.supported_languages:
            self._language = lang

    # Public Methods
    def start(self):
        '''Start listening.'''
        self.results = []
        self.errors = []
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
