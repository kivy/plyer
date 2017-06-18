'''
Fingerprint Scanner
===================

A class that coordinates access to fingerprint hardware.
Fingerprint scanner can be used to lock/unlock devices and apps,
online transactions can be made possible with the help of fingerprint
authentication.

The :class:`Fingerprint` provides access to public methods to use
fingerprint scanner of your device.

Simple Examples
---------------

To enroll a fingerprint::

    >>> from plyer import fingerprint
    >>> fingerprint.register()

To check the presence of fingerprint scanner on your device::

    >>> from plyer import fingerprint
    >>> fingerprint.check_hardware()

To check at least one fingerprint is enrolled in device::

    >>> from plyer import fingerprint
    >>> fingerprint.is_enrolled()

To authenticate the fingerprint::

    >>> from plyer import fingerprint
    >>> fingerprint.authenticate()

'''


class Fingerprint(object):
    '''
    Fingerprint facade.
    '''

    def register(self):
        '''
        Enroll a new fingerprint.
        '''
        return self._register()

    def check_hardware(self):
        '''
        Determine if fingerprint hardware is present and functional.
        '''
        return self._check_hardware()

    def is_enrolled(self):
        '''
        Determine if there is at least one fingerprint enrolled.
        '''
        return self._is_enrolled()

    def authenticate(self):
        '''
        Request authentication of scanned fingerprint.
        '''
        return self._authenticate()

    #private

    def _register(self):
        raise NotImplementedError()

    def _check_hardware(self):
        raise NotImplementedError()

    def _is_enrolled(self):
        raise NotImplementedError()

    def _authenticate(self):
        raise NotImplementedError()
