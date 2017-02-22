class SpatialOrientation(object):
    '''Spatial Orientation facade.

    .. note::
        These settings are generally guidelines, the operating
        system may choose to ignore them, or they may be overridden by
        other system components.

    .. versionadded:: 1.2.4
    '''

    @property
    def orientation(self):
        '''Property that returns values of the current device orientation
        as a (pitch, roll, azimuth) tuple.
        Pitch has range from -180 to 180 (X angle).
        Roll has range from -90 to 90 (Y angle).
        Azimuth from 0 to 360 (Z angle).
        Returns (None, None, None) if no data is currently available.
        '''
        return self._get_orientation() or (None, None, None)

    def _get_orientation(self):
        raise  NotImplementedError()

    def enable_listener(self):
        '''Enable the orientation sensor.
        '''
        self._enable_listener()

    def _enable_listener(self, **kwargs):
        raise NotImplementedError()

    def disable_listener(self):
        '''Disable the orientation sensor.
        '''
        self._disable_listener()

    def _disable_listener(self, **kwargs):
        raise NotImplementedError()
