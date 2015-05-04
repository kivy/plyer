class GPS(object):
    '''GPS facade.

    .. versionadded:: 1.1

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

    def configure(self, on_location, on_status=None):
        '''Configure the GPS object. This method should be called before
        :meth:`start`.

        :param on_location: Function to call when receiving a new location
        :param on_status: Function to call when a status message is received
        :type on_location: callable, multiples keys/value will be passed.
        :type on_status: callable, args are "message-type", "status"

        .. warning::

            The `on_location` and `on_status` callables might be called from
            another thread than the thread used for creating the GPS object.
        '''
        self.on_location = on_location
        self.on_status = on_status
        self._configure()

    def start(self):
        '''Start the GPS location updates.
        '''
        self._start()

    def stop(self):
        '''Stop the GPS location updates.
        '''
        self._stop()

    # private

    def _configure(self):
        raise NotImplementedError()

    def _start(self):
        raise NotImplementedError()

    def _stop(self):
        raise NotImplementedError()
