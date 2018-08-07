'''
Module of MacOS API for plyer.bluetooth.
'''

from subprocess import Popen, PIPE
from plyer.facades import Bluetooth
from plyer.utils import whereis_exe

from os import environ


class OSXBluetooth(Bluetooth):
    '''
    Implementation of MacOS bluetooth API.
    '''

    def _get_info(self):
        old_lang = environ.get('LANG')
        environ['LANG'] = 'C'

        sys_profiler_process = Popen(
            ["system_profiler", "SPBluetoothDataType"],
            stdout=PIPE
        )
        grep_process = Popen(
            ["grep", "Bluetooth Power"],
            stdin=sys_profiler_process.stdout, stdout=PIPE
        )
        sys_profiler_process.stdout.close()
        output = grep_process.communicate()[0]

        if old_lang is None:
            environ.pop('LANG')
        else:
            environ['LANG'] = old_lang

        if output:
            return output.split()[2]
        else:
            return None


def instance():
    '''
    Instance for facade proxy.
    '''
    import sys
    if whereis_exe('system_profiler'):
        return OSXBluetooth()
    sys.stderr.write("system_profiler not found.")
    return Bluetooth()
