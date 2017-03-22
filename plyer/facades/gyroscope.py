'''
Gyroscope
============

The gyroscope measures the rate of rotation in rad/s around a device's x, y,
and z axis.

The :class:`Gyroscope` provides access to public methods to
use gyroscope of your device.

Simple Examples
---------------

To enable gyroscope::

    >>> from plyer import gyroscope
    >>> gyroscope.enable()

To disable gyroscope::

    >>> gyroscope.disable()

To get the rate of rotation along the three axes::

    >>> gyroscope.rotation
    (-0.0034587313421070576, -0.0073830625042319298, 0.0046892408281564713)

'''


class Gyroscope(object):
    '''
    Gyroscope facade.

    .. versionadded:: 1.2.0
    '''

    @property
    def rotation(self):
        '''
        Property that returns values of the current Gyroscope sensors, as
        a (x, y, z) tuple. Returns (None, None, None) if no data is currently
        available.
        '''
        return self.get_rotation()

    def enable(self):
        '''
        Activate the Gyroscope sensor.
        '''
        self._enable()

    def disable(self):
        '''
        Disable the Gyroscope sensor.
        '''
        self._disable()

    def get_rotation(self):
        return self._get_rotation()

    # private

    def _enable(self):
        raise NotImplementedError()

    def _disable(self):
        raise NotImplementedError()

    def _get_rotation(self):
        raise NotImplementedError()
