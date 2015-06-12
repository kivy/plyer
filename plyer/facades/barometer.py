class Barometer(object):
    '''Barometer facade.

    Barometer sensor is used to measure air pressure.

    With method `enable` you turns on step sensor and respectively 'disable'
    method stops the sensor.

    Use property `pressure` to get current air pressure.

    .. versionadded:: 1.2.5
    '''

    @property
    def pressure(self):
        '''Number of steps traveled since enable sensor.

        :return: total number of steps.
        '''
        return self._get_pressure()

    def _get_pressure(self, **kwargs):
        raise NotImplementedError()

    def _enable(self, **kwargs):
        raise NotImplementedError()

    def enable(self):
        '''Enable barometer sensor.'''
        self._enable()

    def _disable(self, **kwargs):
        raise NotImplementedError()

    def disable(self):
        '''Disable barometer sensor.'''
        self._disable()
