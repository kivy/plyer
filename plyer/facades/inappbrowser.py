class InAppBrowser(object):
    '''facade for Inapp-browsing'''

    def access_url(self,url=None):
        '''
        Opens the provided url
        params :
            url as string
        '''
        self._access_url(url=url)

    def _access_url(self,**kwargs):
        raise NotImplementedError()
