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
iOS

Example Usage
-------------

To start a VOIP call:

    >>> from plyer import voip
    >>> voip.start_call(
            dst_address = "192.168.1.67"
            dst_port = 8080
        )

To end a VOIP call:

    >>> voip.end_call()
"""


class Voip:
    '''
    Voip facade.
    '''

    def start_call(self, **kwargs):
        '''
        Start a VOIP call. This establishes the connection, microphone
        stream, and speaker stream.

        :param dst_address: Sets server IP address or root domain
        :type dst_address: string
        :param dst_port: Sets server destination port
        :type dst_port: integer
        :param client_id: Allows authentication of caller
        :type client_id: string
        :param timeout: Limits time for connection
        :type timeout: integer
        :param ssl: Enables SSL/TLS
        :type ssl: boolean
        :param tls_version: Allows TLS version selection
        :type tls_version: string
        :param debug: Displays debug logs
        :type debug: boolean
        '''
        self._start_call(**kwargs)

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
