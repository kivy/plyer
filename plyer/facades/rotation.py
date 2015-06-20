class Rotation(object):
    '''Rotation facade.

    Rotation sensor is used to get the azimuth, pitch, and roll of the device.

    Definition of the coordinate system used below :

    X is defined as the vector product Y.Z (It is tangential to the ground at the device's current location and roughly
    points East).
    Y is tangential to the ground at the device's current location and points towards magnetic north.
    Z points towards the sky and is perpendicular to the ground.

    The rotation values IN DEGREES are given as a tuple :
    values[0]: Azimuth, angle between the magnetic north direction and the y-axis, around the z-axis (0 to 359).
    values[1]: Pitch, rotation around X-axis (-90 to 90), with positive values when the Z-axis moves toward the Y-axis
    values[2]: Roll, rotation around the X-axis (-180 to 180) increasing as the device moves clockwise.


    .. versionadded:: 1.2.5
    '''

    @property
    def rotation(self):
        '''Property that returns values of the current rotation
        as (azimuth, pitch, roll) tuple.
        Returns (None, None, None) if no data is currently available.
        '''
        return self.get_rotation()

    def enable(self):
        '''Activate the rotation sensor.
        '''
        self._enable()

    def disable(self):
        '''Disable the rotation sensor.
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