class Battery(object):
    '''Battery info facade.'''

    @property
    def status(self):
        '''Property that contains a dict with the following fields:
             * **isCharging** *(bool)*: Battery is charging
             * **percentage** *(float)*: Battery charge remaining

            .. warning::
                If any of the fields is not readable, it is set as
                None.
        '''
        return self.get_state()

    def get_state(self):
        return self._get_state()

    #private

    def _get_state(self):
        raise NotImplementedError()
