'''
Audio
=====

The :class:`Audio` is used for recording audio.

Default path for recording is set in platform implementation.

.. note::
        On Android the `RECORD_AUDIO` permission is needed.

Simple Examples
---------------

To start recording::

    >>> from plyer import audio
    >>> audio.start()

To stop recording::

    >>> audio.stop()

To play recording::

    >>> audio.play()

To get the file path::

    >>> audio.file_path
    '/sdcard/testrecorder.3gp'

Te set the file path::

    >>> file_path = path/to/folder
    >>> audio.file_path = file_path

'''


class Audio(object):
    '''
    Audio facade.
    '''

    state = 'ready'
    _file_path = ''

    def __init__(self, file_path):
        super(Audio, self).__init__()
        self._file_path = file_path

    def start(self):
        '''
        Start record.
        '''
        self._start()
        self.state = 'recording'

    def stop(self):
        '''
        Stop record.
        '''
        self._stop()
        self.state = 'ready'

    def play(self):
        '''
        Play current recording.
        '''
        self._play()
        self.state = 'playing'

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, location):
        '''Location of the recording.'''
        assert isinstance(location, (basestring, unicode)), \
            'Location must be string or unicode'
        self._file_path = location

    # private

    def _start(self):
        raise NotImplementedError()

    def _stop(self):
        raise NotImplementedError()

    def _play(self):
        raise NotImplementedError()
