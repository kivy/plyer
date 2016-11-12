'''
Compass
=======

The :class:`Compass` provides access to public methods to use compass of your
device.

Simple Examples
---------------

To enable compass::

    >>> from plyer import compass
    >>> compass.enable()

To disable compass::

    >>> compass.disable()

To get the orientation::

    >>> compass.orientation
    (-23.721826553344727, -5.7114701271057129, -36.749668121337891)

'''


class Compass(object):
    '''Compass facade.

    .. versionadded:: 1.2.0
    '''

    @property
    def orientation(self):
        '''Property that returns values of the current compass
        (magnetic field) sensors, as a (x, y, z) tuple.
        Returns (None, None, None) if no data is currently available.
        '''
        return self.get_orientation()

    def enable(self):
        '''Activate the compass sensor.
        '''
        self._enable()

    def disable(self):
        '''Disable the compass sensor.
        '''
        self._disable()

    def get_orientation(self):
        return self._get_orientation()

    # private

    def _enable(self):
        raise NotImplementedError()

    def _disable(self):
        raise NotImplementedError()

    def _get_orientation(self):
        raise NotImplementedError()
