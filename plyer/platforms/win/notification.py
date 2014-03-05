from threading import Thread as thread

from plyer.facades import Notification
from plyer.platforms.win.libs.balloontip import balloon_tip


class WindowsNotification(Notification):
    def _notify(self, **kwargs):
        thread(target=balloon_tip, kwargs=kwargs).start()


def instance():
    return WindowsNotification()
