'''
User Acceleration
=================

The acceleration that the user is giving to the device.

The total acceleration of the device is equal to gravity plus the acceleration
the user imparts to the device.

The :class:`UserAcceleration` provides access to public methods to use the
user acceleration of your device.

Simple Examples
---------------

To enable user acceleration::

    >>> from plyer import useracceleration
    >>> useracceleration.enable()

To disable user acceleration::

    >>> from plyer import useracceleration
    >>> useracceleration.disable()

To get the user acceleration::

    >>> from plyer import useracceleration
    >>> useracceleration.acceleration

'''


class UserAcceleration(object):
    '''
    User Acceleration facade.

    .. version added:: 1.3.1
    '''

    @property
    def acceleration(self):
        '''
        Property that returns values of the current User Acceleration, as a
        (x, y, z) tuple. Returns (None, None, None) if no data is currently
        available.
        '''
        return self.get_acceleration()

    def enable(self):
        '''
        Activate the sensor.
        '''
        self._enable()

    def disable(self):
        '''
        Disable the sensor.
        '''
        self._disable()

    def get_acceleration(self):
        return self._get_acceleration()

    #private

    def _enable(self):
        raise NotImplementedError()

    def _disable(self):
        raise NotImplementedError()

    def _get_acceleration(self):
        raise NotImplementedError()
