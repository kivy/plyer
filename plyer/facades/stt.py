class STT(object):
    '''SpeechToText facade.
    '''

    def start_listening(self):
        '''
        Tells the speech recognition engine to begin listening for commands.
        '''
        self._start_listening()

    def stop_listening(self):
        '''
        Tells the speech recognition engine to suspend listening for commands.
        '''
        self._stop_listening()

    def set_commands(self):
        '''
        '''
        self._set_commands()

    def display_commands_title(self):
        '''
        '''
        self._display_commands_title()

    def display_commnds(self):
        '''
        '''
        self._display_commnds()

    # private

    def _start_listening(self, **kwargs):
        raise NotImplementedError()

    def _stop_listening(self, **kwargs):
        raise NotImplementedError()

    def _set_commands(self, **kwargs):
        raise NotImplementedError()

    def _display_commands_title(self, **kwargs):
        raise NotImplementedError()

    def _display_commands(self, **kwargs):
        raise NotImplementedError()
