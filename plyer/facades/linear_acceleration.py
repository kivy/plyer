'''
Linear Acceleration
============

The linear acceleration is a motion sensor that detects the change (delta) in
movement relative to the current device linear acceleration,in three dimensions
along the x, y, and z axis but excluding gravity.

The :class:`LinearAcceleration` provides access to public methods to
use linear acceleration of your device.

'''


class LinearAcceleration(object):
    '''
    Linear Accleration facade.
    '''

    @property
    def acceleration(self):
        '''
        Property that returns values of the current linear acceleration
        sensors, as a (x, y, z) tuple. Returns (None, None, None)
        if no data is currently available.
        '''
        return self.get_acceleration()

    def enable(self):
        '''
        Activate the linear acceleration sensor. Throws an error if the
        hardware is not available or not implemented on.
        '''
        self._enable()

    def disable(self):
        '''
        Disable the linear acceleration sensor.
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
