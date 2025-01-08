'''
Module of iOS API for plyer.maps.
'''

import webbrowser
from plyer.facades import Maps
from urllib.parse import quote_plus


class iOSMaps(Maps):
    '''
    Implementation of iOS Maps API.
    '''

    def _open_by_address(self, address, **kwargs):
        '''
        :param address: An address string that geolocation can understand.
        '''

        address = quote_plus(address, safe=',')
        maps_address = 'http://maps.apple.com/?address=' + address

        webbrowser.open(maps_address)

    def _open_by_lat_long(self, latitude, longitude, **kwargs):
        '''
        Open a coordinate span denoting a latitudinal delta and a
        longitudinal delta (similar to MKCoordinateSpan)

        :param name: (optional), will set the name of the dropped pin
        '''

        name = kwargs.get("name", "Selected Location")
        maps_address = 'http://maps.apple.com/?ll={},{}&q={}'.format(
            latitude, longitude, name)

        webbrowser.open(maps_address)

    def _search(self, query, **kwargs):
        '''
        :param query: A string that describes the search object (ex. "Pizza")

        :param latitude: (optional), narrow down query within area,
        MUST BE USED WITH LONGITUDE

        :param longitude: (optional), narrow down query within area,
        MUST BE USED WITH LATITUDE
        '''

        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')

        query = quote_plus(query, safe=',')
        maps_address = 'http://maps.apple.com/?q=' + query

        if latitude is not None and longitude is not None:
            maps_address += '&sll={},{}'.format(latitude, longitude)

        webbrowser.open(maps_address)

    def _route(self, saddr, daddr, **kwargs):
        '''
        :param saddr: can be given as 'address' or 'lat,long'
        :param daddr: can be given as 'address' or 'lat,long'
        '''
        saddr = quote_plus(saddr, safe=',')
        daddr = quote_plus(daddr, safe=',')

        maps_address = 'http://maps.apple.com/?saddr={}&daddr={}'.format(
                                                            saddr, daddr)
        webbrowser.open(maps_address)


def instance():
    '''
    Instance for facade proxy.
    '''
    return iOSMaps()
