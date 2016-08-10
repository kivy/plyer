class Sharing(object):
    ''' Sharing facade.
    .. note::
        On Android your app needs no special permissions.
    '''

    def share_text(self, extra_subject='', extra_text=''):
        '''
        This method is used to share text among applications.
        Params:
            Expects a String `extra_subject` for example: "Subject"
            Expects a String `extra_text` for example: "Message"
        '''
        self._share_text(extra_subject=extra_subject, extra_text=extra_text)

    def share_images(self, images):
        '''
        This method is used to share one or multiple images.
        Params:
            Expects a list `images` for example:
            ['path/to/the/image/kivy.jpg', 'path/to/the/image/plyer.png']
        '''
        self._share_images(images=images)

    def share_files(self, files):
        '''
        This method is used to share one or multiple files.
        Params:
            Expects a list `files` for example:
            ['path/to/the/file/song.mp3', 'path/to/the/file/234232.ogg']
        '''
        self._share_files(files=files)

    # private

    def _share_text(self, **kwargs):
        raise NotImplementedError()

    def _share_images(self, **kwargs):
        raise NotImplementedError()

    def _share_files(self, **kwargs):
        raise NotImplementedError()
