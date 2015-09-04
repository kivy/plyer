class Gallery(object):
    '''Gallery facade.
    '''

    def choose_image(self, filename, on_complete):
        '''Ask the OS to select a image using inguilt gallery chooser, and store
            it at filename. When the selection is done, on_complete will be
            called with the filename as an argument. If the callback returns
            True, the filename will be unlinked.

            :param filename: Name of the image file
            :param on_complete: Callback that will be called when the operation
            is completed.

            :type filename: str
            :type on_complete: callable
            '''
        self._choose_image(
            filename=filename, on_complete=on_complete)

    def _video(self, filename, on_complete):
        '''Ask the OS to select a video, from os gallery and store it at
            filename.

            When the capture is done, on_complete will be called with the
            filename as an argument. If the callback returns True, the filename
            will be unlinked.

            :param filename: Name of the video file
            :param on_complete: Callback that will be called when the operation
            is done.

            :type filename: str
            :type on_complete: callable
            '''
        self._choose_video(filename=filename, on_complete=on_complete)

    # private

    def _choose_image(self, **kwargs):
        raise NotImplementedError()

    def _choose_video(self, **kwargs):
        raise NotImplementedError()
