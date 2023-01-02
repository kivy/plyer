'''
Maps
=======
The :class:`Maps` creates a client for accessing the default Maps API.

Depending on the platform, holds features such as opening a location by
address & latitude/longitude, create queries, or find directions between
two points

'''


class Maps:
    '''
    Maps facade.
    '''

    def open_by_address(self, address, **kwargs):
        '''
        Open the specificed location by address in the default Maps API
        '''
        self._open_by_address(address, **kwargs)

    def open_by_lat_long(self, latitude, longitude, **kwargs):
        '''
        Open the specificed location by latitude & longitude coordinates
        in the default Maps API
        '''
        self._open_by_lat_long(latitude, longitude, **kwargs)

    def search(self, query, **kwargs):
        '''
        The query. This parameter is treated as if its value had been typed
        into the Maps search field by the user.

        Note that query=* is not supported
        '''
        self._search(query, **kwargs)

    def _open_by_address(self, address, **kwargs):
        raise NotImplementedError()

    def _open_by_lat_long(self, latitude, longitude, **kwargs):
        raise NotImplementedError()

    def _search(self, query, **kwargs):
        raise NotImplementedError()
