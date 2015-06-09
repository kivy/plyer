class MagneticField(object):
    '''MagneticField facade.
    
    .. versionadded:: 1.2.5
    '''

    @property
    def magnetic(self):
        '''Property that returns values of the current magnetic field
        sensors, as a (x, y, z) tuple. Returns (None, None, None)
        if no data is currently available.
        '''
        return self._get_magnetic()

    def enable(self):
        '''Activate the magnetic field sensor. Throws an error if the
        hardware is not available or not implemented on.
        '''
        self._enable()

    def disable(self):
        '''Disable the magnetic field sensor.
        '''
        self._disable()

    # private

    def _enable(self):
        raise NotImplementedError()

    def _disable(self):
        raise NotImplementedError()

    def _get_magnetic(self):
        raise NotImplementedError()
