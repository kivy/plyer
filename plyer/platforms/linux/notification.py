import subprocess
from plyer.facades import Notification
from plyer.utils import whereis_exe


class NotifySendNotification(Notification):
    ''' Pops up a notification using notify-send
    '''
    def _notify(self, **kwargs):
        subprocess.call(["notify-send",
                         kwargs.get('title'),
                         kwargs.get('message')])


class NotifyDbus(Notification):
    ''' notify using dbus interface
    '''

    def _notify(self, **kwargs):
        summary = kwargs.get('title', "title")
        body = kwargs.get('message', "body")
        app_name = kwargs.get('app_name', '')
        app_icon = kwargs.get('app_icon', '')
        timeout = kwargs.get('timeout', 5000)
        actions = kwargs.get('actions', [])
        hints = kwargs.get('hints', [])
        replaces_id = kwargs.get('replaces_id', 0)

        _bus_name = 'org.freedesktop.Notifications'
        _object_path = '/org/freedesktop/Notifications'
        _interface_name = _bus_name

        import dbus
        session_bus = dbus.SessionBus()
        obj = session_bus.get_object(_bus_name, _object_path)
        interface = dbus.Interface(obj, _interface_name)
        interface.Notify(app_name, replaces_id, app_icon,
            summary, body, actions, hints, timeout)


def instance():
    import sys
    try:
        import dbus
        return NotifyDbus()
    except ImportError:
        sys.stderr.write("python-dbus not installed. try:"
                         "`sudo pip install python-dbus`.")
    if whereis_exe('notify-send'):
        return NotifySendNotification()
    sys.stderr.write("notify-send not found.")
    return Notification()
