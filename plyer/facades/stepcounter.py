class StepCounter(object):
    '''Step Counter facade.
    Step Counter sensor returns the number of steps taken by
    the user since the last reboot while activated.

    If you want to continuously track the number of steps over a
    long period of time, do NOT unregister for this sensor,
    so that it keeps counting steps in the background even when
    the AP is in suspend mode and report the aggregate count when the AP is awake. 

    With method `enable` you can turn on Rotation Vector sensor and 'disable'
    method stops the sensor.
    Use property `vector` to get rotation vector values.
    '''

    @property
    def count(self):
        '''Current number of steps taken by the user
        since the last reboot while activated
        '''
        return self._get_count()

    def enable(self):
        '''Enable Step Counter sensor.'''
        self._enable()

    def disable(self):
        '''Disable Step Counter sensor.'''
        self._disable()

    #private
        
    def _get_count(self, **kwargs):
        raise NotImplementedError()

    def _enable(self, **kwargs):
        raise NotImplementedError()

    def _disable(self, **kwargs):
        raise NotImplementedError()
