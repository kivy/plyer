import unittest

import sys
import os.path as op

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)

from plyer.utils import platform

from plyer.facades.notification import Notification as NFacade
from plyer import notification

if platform == 'win':
    from plyer.platforms.win.notification import WindowsNotification
elif platform == 'linux':
    from plyer.platforms.linux.notification import (
        NotifySendNotification,
        NotifyDbus
    )


class Test(unittest.TestCase):
    def show_notification(self, instance):
        path = op.dirname(op.abspath(__file__))
        instance.notify(
            title='title',
            message='My Message\nis multiline',
            app_name='Plyer Test',
            app_icon=op.join(path, 'images', 'kivy32.ico'),
            timeout=3
        )

    def test_notification_windows(self):
        if platform != 'win':
            return

        self.assertIsNot(notification, NFacade)
        self.show_notification(WindowsNotification())

    def test_notification_dbus(self):
        if platform != 'linux':
            return

        self.assertIsNot(notification, NFacade)
        self.show_notification(NotifyDbus())

    def test_notification_notifysend(self):
        if platform != 'linux':
            return

        self.assertIsNot(notification, NFacade)
        self.show_notification(NotifySendNotification())


if __name__ == '__main__':
    unittest.main()
