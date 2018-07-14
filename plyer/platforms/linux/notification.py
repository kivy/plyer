'''
Module of Linux API for plyer.notification.
'''

import warnings
import subprocess
from plyer.facades import Notification
from plyer.utils import whereis_exe


class NotifySendNotification(Notification):
    # pylint: disable=too-few-public-methods
    '''
    Implementation of Linux notification API
    using notify-send binary.
    '''
    def _notify(self, **kwargs):
        subprocess.call([
            "notify-send", kwargs.get('title'), kwargs.get('message')
        ])


class NotifyDbus(Notification):
    # pylint: disable=too-few-public-methods
    '''
    Implementation of Linux notification API
    using dbus library and dbus-python wrapper.
    '''

    def _notify(self, **kwargs):
        # pylint: disable=too-many-locals
        summary = kwargs.get('title', "title")
        body = kwargs.get('message', "body")
        app_name = kwargs.get('app_name', '')
        app_icon = kwargs.get('app_icon', '')
        timeout = kwargs.get('timeout', 10)
        actions = kwargs.get('actions', [])
        hints = kwargs.get('hints', [])
        replaces_id = kwargs.get('replaces_id', 0)

        _bus_name = 'org.freedesktop.Notifications'
        _object_path = '/org/freedesktop/Notifications'
        _interface_name = _bus_name

        import dbus  # pylint: disable=import-error
        session_bus = dbus.SessionBus()
        obj = session_bus.get_object(_bus_name, _object_path)
        interface = dbus.Interface(obj, _interface_name)
        interface.Notify(
            app_name, replaces_id, app_icon,
            summary, body, actions,
            hints, timeout * 1000
        )


def instance():
    '''
    Instance for facade proxy.
    '''
    try:
        import dbus  # pylint: disable=unused-variable
        return NotifyDbus()
    except ImportError:
        msg = ("The Python dbus package is not installed.\n"
               "Try installing it with your distribution's package manager, "
               "it is usually called python-dbus or python3-dbus, but you "
               "might have to try dbus-python instead, e.g. when using pip.")
        warnings.warn(msg)

    if whereis_exe('notify-send'):
        return NotifySendNotification()
    warnings.warn("notify-send not found.")
    return Notification()
