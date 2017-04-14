'''
ScreenShot
=====

The :class:`ScreenShot` is used for recording audio.

Default path for taking screenshot is set in platform implementation.

Simple Examples
---------------

To get the file path::

    >>> screenshot.file_path
    '/sdcard/test.jpg'

To set the file path::

    >>> import os
    >>> current_list = os.listdir('.')
    ['/sdcard/testrecorder.jpg', '/sdcard/testrecorder1.jpg',
    '/sdcard/testrecorder2.jpg', '/sdcard/testrecorder3.jpg']
    >>> file_path = current_list[2]
    >>> screenshot.file_path = file_path

To take screenshot::

    >>> from plyer import screenshot
    >>> screenshot.take_shot()
'''


class Screenshot(object):
    '''
    ScreenShot facade.
    '''
    _file_path = ''

    def __init__(self, file_path):
        super(Screenshot, self).__init__()
        self._file_path = file_path

    def take(self):
        self._take()

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, location):
        '''
        Location of the screenshot.
        '''
        self._file_path = location

    # private

    def _take(self, **kwargs):
        raise NotImplementedError()
