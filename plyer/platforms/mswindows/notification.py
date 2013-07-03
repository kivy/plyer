from plyer.facades import Notification
from libs import balloontip


class WindowsNotification(Notification):
    def _notify(self, **kwargs):
        ballontip.balloon_tip(kwargs.get('title'), kwargs.get('message'))


def instance():
    return WindowsNotification()

