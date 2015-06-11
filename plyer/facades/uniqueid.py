class UniqueID(object):
    '''UniqueID facade.

    Returns the following depending on the platform:

    * **Android**: Android ID
    * **OS X**: Serial number of the device
    * **Linux**: Serial number using lshw
    * **Windows**: MachineGUID from regkey

    .. versionadded:: 1.2.0

    .. versionchanged:: 1.2.4
        On Android returns Android ID instead of IMEI.
    '''

    @property
    def id(self):
        '''Property that returns the unique id of the platform.
        '''
        return self.get_uid()

    def get_uid(self):
        return self._get_uid()

    # private

    def _get_uid(self, **kwargs):
        raise NotImplementedError()
