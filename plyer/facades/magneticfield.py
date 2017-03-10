class MagneticField(object):
    '''Magnetic Field facade.
    Magnetic Field sensor is used to measure the magnetic field as
    Geomagnetic field strength along the x axis,
    Geomagnetic field strength along the y axis,
    Geomagnetic field strength along the z axis.
    With method `enable` you can turn on Magnetic Field sensor and 'disable'
    method stops the sensor.
    Use property `field` to get magnetic field values.
    '''

    @property
    def field(self):
        '''Current value of magnetic field'''
        return self._get_field()

    def enable(self):
        '''Enable Magnetic Field sensor.'''
        self._enable()

    def disable(self):
        '''Disable Magnetic Field sensor.'''
        self._disable()

    #private
    def _get_field(self, **kwargs):
        raise NotImplementedError()

    def _enable(self, **kwargs):
        raise NotImplementedError()

    def _disable(self, **kwargs):
        raise NotImplementedError()
