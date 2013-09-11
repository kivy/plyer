import thread

from plyer.facades import Notification
from libs.balloontip import balloon_tip


class WindowsNotification(Notification):
    def _notify(self, **kwargs):
        thread.start_new_thread(balloon_tip,
                                (kwargs.get('title'), kwargs.get('message')))


def instance():
    return WindowsNotification()
