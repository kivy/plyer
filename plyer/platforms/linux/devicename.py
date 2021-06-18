'''
Module of Linux API for plyer.devicename.
'''

import socket
from plyer.facades import DeviceName


class LinuxDeviceName(DeviceName):
    '''
    Implementation of Linux DeviceName API.
    '''

    def _get_device_name(self):
        hostname = None
        if not socket.gethostname():
            hostname = socket.gethostname()
        return hostname


def instance():
    '''
    Instance for facade proxy.
    '''
    return LinuxDeviceName()
