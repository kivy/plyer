class Orientation(object):
    '''Orientation facade.

    .. note::
        These settings are generally guidelines, the operating
        system may choose to ignore them, or they may be overridden by
        other system components.

    .. versionadded:: 1.2.4
    '''

    orientation = None
    '''Current orientation.'''

    def set_landscape(self, reverse=False):
        '''Rotate the app to a landscape orientation.

        :param reverse: If True, uses the opposite of the natural
                        orientation.
        '''
        self._set_landscape(reverse=reverse)

    def _set_landscape(self, **kwargs):
        raise NotImplementedError()

    def set_portrait(self, reverse=False):
        '''Rotate the app to a portrait orientation.

        :param reverse: If True, uses the opposite of the natural
                        orientation.
        '''
        self._set_portrait(reverse=reverse)

    def _set_portrait(self, **kwargs):
        raise NotImplementedError()

    def set_sensor(self, mode='any'):
        '''Rotate freely following sensor information from the device.

        :param mode: The rotation mode, should be one of 'any' (rotate
                     to any orientation), 'landscape' (choose nearest
                     landscape mode) or 'portrait' (choose nearest
                     portrait mode). Defaults to 'any'.
        '''
        self._set_sensor(mode=mode)

    def _set_sensor(self, **kwargs):
        raise NotImplementedError()
