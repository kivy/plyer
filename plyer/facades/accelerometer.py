class Accelerometer(object):
    '''Accelerometer facade.
    '''

    @property
    def acceleration(self):
        '''Property that returns values of the current acceleration
        sensors, as a (x, y, z) tuple. Returns (None, None, None)
        if no data is currently available.
        '''
        return self.get_acceleration()

    def enable(self):
        '''Activate the accelerometer sensor. Throws an error if the
        hardware is not available or not implemented on.
        '''
        self._enable()

    def disable(self):
        '''Disable the accelerometer sensor.
        '''
        self._disable()

    def get_acceleration(self):
        return self._get_acceleration()

    # private

    def _enable(self):
        raise NotImplementedError()

    def _disable(self):
        raise NotImplementedError()

    def _get_acceleration(self):
        raise NotImplementedError()
