class Sharing(object):
    ''' Sharing facade.
    .. note::
        On Android your app needs the CALL_PHONE permission in order to
        make calls.
    '''

    def share_text(self, extra_subject='', extra_text=''):
        self._share_text(extra_subject=extra_subject, extra_text=extra_text)

    def share_images(self, **kwargs):
        self._share_images(**kwargs)

    # private

    def _share_text(self, **kwargs):
        raise NotImplementedError()

    def _share_images(self, *args, **kwargs):
        raise NotImplementedError()
