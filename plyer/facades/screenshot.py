'''
ScreenShot
======

The :class:`ScreenShot` is to capture screen shots.

Simple Examples
---------------

Setup callback function.

    >>> from os.path import exists, join
    >>> from plyer import screenshot
    >>> def camera_callback(filepath):
    >>>     if(exists(filepath)):
    >>>         print "saved"
    >>>     else:
    >>>         print "unable to save."
    >>> filepath = 'path/to/your/file'
    >>> # e.g: filepath = join(App.get_running_app().user_data_dir, file_name)

To take screenshot::

    >>> file_name = "test.jpg"
    >>> screenshot.take_picture(filename=file_name,
    >>>                     on_complete=camera_callback)
'''


class ScreenShot(object):
    '''
    ScreenShot facade.
    '''

    def take_shot(self, filename, on_complete):
        '''Ask the OS to capture a screenshot, and store it at filename.

        When the capture is done, on_complete will be called with the filename
        as an argument. If the callback returns True, the filename will be
        unlinked.

        :param filename: Name of the image file
        :param on_complete: Callback that will be called when the operation is
            done

        :type filename: str
        :type on_complete: callable
        '''
        self._take_shot(filename=filename, on_complete=on_complete)

       # private

    def _take_shot(self, **kwargs):
        raise NotImplementedError()
    
