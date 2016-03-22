class InAppBrowser(object):
    '''InAppBrowser facade.'''

    def open_url(self, url=None):
        '''Open an in-app webview to open given url.

        :param url: url (str)

        '''
        self._open_url(url=url)

    # private

    def _open_url(self, **kwargs):
        raise NotImplementedError()
