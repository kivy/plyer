class RelativeHumidity(object):
    '''Relative Humidity facade.
    Relative Humidity sensor returns percentage of humidity.
    With method `enable` you can turn on Relative Humidity sensor and 'disable'
    method stops the sensor.
    Use property `humidity` to get relative humidity value.
    '''

    @property
    def humidity(self):
        '''Current percentage of humidity'''
        return self._get_humidity()

    def enable(self):
        '''Enable Relative Humidity sensor.'''
        self._enable()

    def disable(self):
        '''Disable Relative Humidity sensor.'''
        self._disable()

    #private
    def _get_humidity(self, **kwargs):
        raise NotImplementedError()

    def _enable(self, **kwargs):
        raise NotImplementedError()

    def _disable(self, **kwargs):
        raise NotImplementedError()
