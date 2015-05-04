class UniqueID(object):
    '''UniqueID facade.

    Returns the following depending on the platform:

    * **Android**: IMEI
    * **Mac OSX**: Serial number of the device
    * **Linux**: Serial number using lshw
    * **Windows**: MachineGUID from regkey

    .. note::
        On Android your app needs the READ_PHONE_STATE permission

    .. versionadded:: 1.2.0
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
