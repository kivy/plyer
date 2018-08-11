'''
CPU
===

Simple Example
---------------

To get CPU count::
    >>> from plyer import cpu
    >>> # 1 socket, 1 core per socket, 2 threads per core
    >>> cpu.sockets   # 1 CPU socket (or slot)
    1
    >>> cpu.physical  # 1 CPU socket * 1 core per socket
    1
    >>> cpu.logical   # 1 CPU socket * 1 core per socket * 2 threads per core
    2

Supported Platforms
-------------------

MacOS
Linux
'''


class CPU(object):
    '''
    Facade providing info about sockets, physical and logical
    number of processors.
    '''

    @property
    def sockets(self):
        '''
        Property that contains the count of CPU sockets.
        '''
        return self._sockets()

    @property
    def physical(self):
        '''
        Property that contains the total number of physical cores
        (max core count) in the system.

        .. note:: `sockets * cores per socket`
        '''
        return self._physical()

    @property
    def logical(self):
        '''
        Property that contains the total number of logical cores
        (max thread count) in the system.

        .. note:: `sockets * cores per socket * threads per core`
        '''
        return self._logical()

    # private

    def _sockets(self):
        raise NotImplementedError()

    def _physical(self):
        raise NotImplementedError()

    def _logical(self):
        raise NotImplementedError()

