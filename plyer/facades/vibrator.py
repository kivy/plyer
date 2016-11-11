'''
Vibrator
=======

The :class:`Vibrator` provides access to public methods to use vibrator of your
device.

.. note::
    On Android your app needs the VIBRATE permission to
    access the vibrator.

Simple Examples
---------------

To vibrate your device::

    >>> from plyer import vibrator
    >>> time=2
    >>> vibrator.vibrate(time=time)

To set a pattern::

    >>> vibrator.pattern(pattern=pattern, repeat=repeat)

To know whether vibrator exists or not::

    >>> vibrator.exists()

To cancel vibration::

    >>> vibrator.cancel()

'''


class Vibrator(object):
    '''Vibration facade.
    '''

    def vibrate(self, time=1):
        '''Ask the vibrator to vibrate for the given period.

        :param time: Time to vibrate for, in seconds. Default is 1.
        '''
        self._vibrate(time=time)

    def _vibrate(self, **kwargs):
        raise NotImplementedError()

    def pattern(self, pattern=(0, 1), repeat=-1):
        '''Ask the vibrator to vibrate with the given pattern, with an
        optional repeat.

        :param pattern: Pattern to vibrate with. Should be a list of
            times in seconds. The first number is how long to wait
            before vibrating, and subsequent numbers are times to
            vibrate and not vibrate alternately.
            Defaults to ``[0, 1]``.

        :param repeat: Index at which to repeat the pattern. When the
            vibration pattern reaches this index, it will start again
            from the beginning. Defaults to ``-1``, which means no
            repeat.
        '''
        self._pattern(pattern=pattern, repeat=repeat)

    def _pattern(self, **kwargs):
        raise NotImplementedError()

    def exists(self):
        '''Check if the device has a vibrator. Returns True or
            False.
        '''
        return self._exists()

    def _exists(self, **kwargs):
        raise NotImplementedError()

    def cancel(self):
        '''Cancels any current vibration, and stops the vibrator.'''
        self._cancel()

    def _cancel(self, **kwargs):
        raise NotImplementedError()
