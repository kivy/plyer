class Dirs(object):
    '''Dirs Manager facade.

    .. versionadded:: 1.2.5

    You need to set a `on_location` callback with the :meth:`configure` method.
    This callback will receive a couple of keywords / values, that might be
    different depending of their availability on the targeted platform.
    Lat and lon are always available.

    - lat: latitude of the last location, in degrees
    - lon: longitude of the last location, in degrees
    - speed: speed of the user, in meters/second over ground
    - bearing: bearing in degrees
    - altitude: altitude in meters above the sea level

    Here is an example of the usage of gps::

        from plyer import gps

        def print_locations(**kwargs):
            print 'lat: {lat}, lon: {lon}'.format(**kwargs)

        gps.configure(on_location=print_locations)
        gps.start()
        # later
        gps.stop()
    '''

    def get_private(self, appname, version=None):
        """ get private storage path

        - appname: required for some platforms to make app-named subdir
        while other (like Android) will point to app-specific directory
        automatically, and parameter will be ignored
        """
        return self._get_private(appname, version)

    def get_cache(self, appname, version=None):
        """ get large cache dir

        - appname: required for some platforms to make app-named subdir
        while other (like Android) will point to app-specific directory
        automatically, and parameter will be ignored
        """
        return self._get_cache(appname, version)

    # private

    def _get_private(self, appname=None, version=None):
        raise NotImplementedError()

    def _get_cache(self, appname=None, version=None):
        raise NotImplementedError()
