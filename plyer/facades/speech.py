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

    language = 'en-US'
    '''default language in which platform will try to recognize voice.
    In order to change language pick one from list by using
    `supported_languages` method.
    '''

    _supported_languages = [
        'en-US',
        'pl-PL'
    ]

    _results = []
    '''List of strings found while listening.'''

    _errors = []
    '''List of errors occured while listening.'''

    @property
    def supported_languages(self):
        return self._supported_languages

    # Private Methods
    def _start(self):
        raise NotImplementedError

    def _stop(self):
        raise NotImplementedError

    def _exist(self):
        raise NotImplementedError

    # Public Methods
    def start(self):
        '''Start listening.'''

        self._results = []
        self._errors = []
        self._start()

    def stop(self):
        '''Stop listening.'''
        self._stop()

    def exist(self):
        '''True if Speech Recognition is available.'''
        self._exist()

    def get_results(self):
        '''Return list of found words from voice.

        :rtype: list of strings.
        '''
        return self._results