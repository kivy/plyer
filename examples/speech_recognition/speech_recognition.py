class Speech(object):
    '''Speech Recognition facade.


    .. note:
        Needed permissions for Android: RECORD_AUDIO and NETWORK.
        Network are needed when voice recognize is checked online.
    '''

    language = 'en-US'
    '''default language in which platoform will try to recognize voice.
    In order to change language pick one from list by using
    `supported_languages` method.
    '''

    def supported_languages(self):
        return []

    def start(self):
        '''Start listening.'''

        raise NotImplementedError

    def stop(self):
        '''Stop listening.'''
        raise NotImplementedError

    def exist(self):
        '''True if Speech Recognition is available.'''
        raise NotImplementedError
