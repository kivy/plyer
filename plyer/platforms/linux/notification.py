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


def instance():
    if whereis_exe('notify-send'):
        return NotifySendNotification()
    return Notification()
