
MICROPHONE_STATUS = {
    'prepare': 'prepare',
    'ready': 'ready',
    'pause': 'pause',
    'play': 'play',
    'recording': 'recording',
    'stopped': 'stopped',
}


class Microphone(object):
    """Microphone Facade.
    Used for recording audio.
    Use method `start` to start record and `stop` for stop recording.
    For hear, what you have just recorded use method `play`.
    Use `pause` to pause record and again or `resume` for un-pause.
    Method `info` will inform you about source destination and quality
    of the record.
    Status will tell you about current job of the Microphone.
    .. note::
        You need android permissions: RECORD_AUDIO
    """

    _state = MICROPHONE_STATUS['prepare']
    _file_path = ''

    def __init__(self, file_path):
        super(Microphone, self).__init__()
        self._file_path = file_path

    def start(self):
        """Start record."""
        self._start()

    def _start(self):
        raise NotImplementedError()

    def stop(self):
        """Stop record."""
        self._stop()

    def _stop(self):
        raise NotImplementedError()

    def play(self):
        """Play current recording."""
        self._play()

    def _play(self):
        raise NotImplementedError()

    def pause(self):
        """Pause Record."""
        self._pause()

    def resume(self):
        """Resume recording."""
        self._resume()

    def _resume(self):
        raise NotImplementedError()

    def _pause(self):
        raise NotImplementedError()

    @property
    def info(self):
        """Give info about quality and source destination."""
        return self._info()

    def _info(self):
        raise NotImplementedError()

    @property
    def status(self):
        """Return status of Microphone."""
        return MICROPHONE_STATUS[self._state]

    @status.setter
    def status(self, state):
        self._state = state

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, location):
        assert isinstance(location, (basestring, unicode)), \
            'Location must be string or unicode'
        self._file_path = location
