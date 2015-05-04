class Camera(object):
    '''Camera facade.
    '''

    def take_picture(self, filename, on_complete):
        '''Ask the OS to capture a picture, and store it at filename.

        When the capture is done, on_complete will be called with the filename
        as an argument. If the callback returns True, the filename will be
        unlinked.

        :param filename: Name of the image file
        :param on_complete: Callback that will be called when the operation is
            done

        :type filename: str
        :type on_complete: callable
        '''
        self._take_picture(filename=filename, on_complete=on_complete)

    def take_video(self, filename, on_complete):
        '''Ask the OS to capture a video, and store it at filename.

        When the capture is done, on_complete will be called with the filename
        as an argument. If the callback returns True, the filename will be
        unlinked.

        :param filename: Name of the video file
        :param on_complete: Callback that will be called when the operation is
            done

        :type filename: str
        :type on_complete: callable
        '''
        self._take_video(filename=filename, on_complete=on_complete)

    # private

    def _take_picture(self, **kwargs):
        raise NotImplementedError()

    def _take_video(self, **kwargs):
        raise NotImplementedError()
