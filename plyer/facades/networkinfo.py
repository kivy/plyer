'''
Network Information
===================

This facade gives details about the currently active default data network.
When connected, this network is the default route for outgoing connections.

The :class:`NetworkInfo` provides access to public methods to get network
information of your device.

Simple Examples
---------------

To import facade::

    >>> from plyer import networkinfo

To get extra network information::

    >>> networkinfo.get_extra_info()
        jionet

To get subtype of network::

    >>> networkinfo.get_subtype_name()
        LTE

To get type of network::

    >>> networkinfo.get_type_name()
        MOBILE

To check whether whether network connectivity is possible::

    >>> networkinfo.is_available()
        True

To check whether network connectivity exists and it is possible to establish
connections and pass data::

    >>> networkinfo.is_connected()
        True

To check whether the device is currently roaming on this network.

    >>> networkinfo.is_roaming()
        False
'''


class NetworkInfo(object):
    '''
    Network Information facade
    '''

    def get_extra_info(self):
        '''
        Report the extra information about the network state, if any was
        provided by the lower networking layers.
        '''
        return self._get_extra_info()

    def get_subtype_name(self):
        '''
        Return a human-readable name describing the subtype of the network.
        '''
        return self._get_subtype_name()

    def get_type_name(self):
        '''
        Return a human-readable name describe the type of the network,
        for example "WIFI" or "MOBILE".
        '''
        return self._get_type_name()

    def is_available(self):
        '''
        Indicates whether network connectivity is possible.
        Returns a boolean value.
        '''
        return self._is_available()

    def is_connected(self):
        '''
        Indicates whether network connectivity exists and it is possible to
        establish connections and pass data.
        Returns a boolean value.
        '''
        return self._is_connected()

    def is_roaming(self):
        '''
        Indicates whether the device is currently roaming on this network.
        Returns a boolean value.
        '''
        return self._is_roaming()

    #private

    def _get_extra_info(self):
        raise NotImplementedError()

    def _get_subtype_name(self):
        raise NotImplementedError()

    def _get_type_name(self):
        raise NotImplementedError()

    def _is_available(self):
        raise NotImplementedError()

    def _is_connected(self):
        raise NotImplementedError()

    def _is_roaming(self):
        raise NotImplementedError()
