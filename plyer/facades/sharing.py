class Sharing(object):
    ''' Sharing facade.
    .. note::
        On Android your app needs the CALL_PHONE permission in order to
        make calls.
    '''

    def share_text(self, extra_subject='', extra_text=''):
        self._share_text(extra_subject=extra_subject, extra_text=extra_text)

    def share_images(self, images):
        self._share_images(images=images)

    def share_files(self, files):
        self._share_files(files=files)

    # private

    def _share_text(self, **kwargs):
        raise NotImplementedError()

    def _share_images(self, **kwargs):
        raise NotImplementedError()

    def _share_files(self, **kwargs):
        raise NotImplementedError()
