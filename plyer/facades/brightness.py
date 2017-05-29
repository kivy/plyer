'''
Brightness
==========

This API helps you to control the brightness of your primary display screen.

The :class:`Brightness` provides access to public methods to control the
brightness of screen.

Simple Examples
---------------

To set the brightness level to half of maximum::

    >>> from plyer import brightness
    >>> brightness.set(50)

'''


class Brightness(object):
    '''
    Brightness facade.
    '''

    def set(self, level):
        '''
        Adjust the brightness of the screen.
        Minimum brightnesss level:: 1
        Maximum brightness level:: 100

        :param level: New level of brightness between 1 and 100
        :type level: int
        '''
        return self._set(level)

    #private

    def _set(self, level):
        raise NotImplementedError()
