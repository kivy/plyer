"""
Voip
====

The :class:`VOIP` facade offers a comprehensive suite of methods for
managing VoIP (Voice over IP) calls, including initiating and ending calls, 
managing call streams, handling microphone permissions, and overseeing 
network connections.

Supported Platforms
-------------------
Android

Example Usage
-------------

To start a VOIP call:

    >>> from plyer import Voip
    Client = Voip()
    >>> Client.dst_address = "192.168.1.2"
    >>> Client.dst_port = 8080
    >>> Client.start_call()

To end a VOIP call:

    >>> Client.end_call()
"""

class Voip:
    '''
    Voip facade.
    '''

    def start_call(self):
        '''
        Start a VOIP call. This establishes the connection, microphone
        stream, and speaker stream.
        '''
        self._start_call()

    def end_call(self):
        '''
        End the VOIP call, stopping all streams and closing connections.
        '''
        self._end_call()

    # Private methods implemented by the platform-specific class

    def _start_call(self, **kwargs):
        raise NotImplementedError()

    def _end_call(self):
        raise NotImplementedError()
