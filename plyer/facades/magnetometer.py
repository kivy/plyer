class Magnetometer(object):
    '''Magnetometer facade.
    Magnetometer sensor is used to measure the magnetic field as
    Geomagnetic field strength along the x axis,
    Geomagnetic field strength along the y axis,
    Geomagnetic field strength along the z axis.
    With method `enable` you can turn on Magnetometer sensor and 'disable'
    method stops the sensor.
    Use property `field` to get magnetic field values.
    '''

    @property
    def field(self):
        '''Current value of Magnetometer'''
        return self._get_field()

    def enable(self):
        '''Enable Magnetometer sensor.'''
        self._enable()

    def disable(self):
        '''Disable Magnetometer sensor.'''
        self._disable()

    #private
    def _get_field(self, **kwargs):
        raise NotImplementedError()

    def _enable(self, **kwargs):
        raise NotImplementedError()

    def _disable(self, **kwargs):
        raise NotImplementedError()
