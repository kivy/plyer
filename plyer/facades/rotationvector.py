class RotationVector(object):
    '''Rotation Vector facade.
    Rotation Vector sensor is used to measure the rotation vector as
    Rotation vector component along the x axis (x * sin(θ/2)),
    Rotation vector component along the y axis (y * sin(θ/2)),
    Rotation vector component along the z axis (z * sin(θ/2)),
    Scalar component of the rotation vector ((cos(θ/2)).
    With method `enable` you can turn on Rotation Vector sensor and 'disable'
    method stops the sensor.
    Use property `vector` to get rotation vector values.
    '''

    @property
    def vector(self):
        '''Current value of rotation vector'''
        return self._get_vector()

    def enable(self):
        '''Enable Rotation Vector sensor.'''
        self._enable()

    def disable(self):
        '''Disable Rotation Vector sensor.'''
        self._disable()

    #private
        
    def _get_vector(self, **kwargs):
        raise NotImplementedError()

    def _enable(self, **kwargs):
        raise NotImplementedError()

    def _disable(self, **kwargs):
        raise NotImplementedError()
