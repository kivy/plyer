class InAppBrowser(object):
    '''facade for Inapp-browsing'''

    def open_url(self, url=None):
        '''
        Opens the provided url
        params :
            url as string
        '''
        self._open_url(url=url)

    def _open_url(self, **kwargs):
        raise NotImplementedError()
