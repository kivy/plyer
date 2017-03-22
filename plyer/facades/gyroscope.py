'''
Gyroscope
============

The gyroscope measures the rate of rotation in rad/s around a device's x, y,
and z axis.

Rotation is positive in the counter-clockwise direction (right-hand rule).
That is, an observer looking from some positive location on the x, y or z axis
at a device positioned on the origin would report positive rotation if the
device appeared to be rotating counter clockwise.

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

To get the uncalibrated rate of rotation along the three axes along with the
drift compensation::

    >>> gyroscope.rotationUncalib
    ()
    where the first three values show the rate of rotation w/o drift
    compensation and the last three show the estimated drift along the three
    axes.
'''


class Gyroscope(object):
    '''
    Gyroscope facade.

    .. versionadded:: 1.2.0
    '''

    @property
    def rotation(self):
        '''
        Property that returns the rate of rotation around the device's local
        X, Y and Z axis.

        Along x-axis: angular speed around the X axis in rad/s
        Along y-axis: angular speed around the Y axis in rad/s
        Along z-axis: angular speed around the Z axis in rad/s

        Returns (None, None, None) if no data is currently available.
        '''
        return self.get_rotation()

    @property
    def rotationUncalib(self):
        '''
        Property that returns the current rate of rotation around the X, Y and
        Z axis. An estimation of the drift on each axis is reported as well.

        Along x-axis: angular speed (w/o drift compensation) around the X axis
                      in rad/s
        Along y-axis: angular speed (w/o drift compensation) around the Y axis
                      in rad/s
        Along z-axis: angular speed (w/o drift compensation) around the Z axis
                      in rad/s

        Along x-axis: estimated drift around X axis in rad/s
        Along y-axis: estimated drift around Y axis in rad/s
        Along z-axis: estimated drift around Z axis in rad/s

        Returns (None, None, None, None, None, None) if no data is currently
        available.
        '''
        return self.get_rotationUncalib()

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

    def get_rotationUncalib(self):
        return self._get_rotationUncalib()

    # private

    def _enable(self):
        raise NotImplementedError()

    def _disable(self):
        raise NotImplementedError()

    def _get_rotation(self):
        raise NotImplementedError()

    def _get_rotationUncalib(self):
        raise NotImplementedError()
