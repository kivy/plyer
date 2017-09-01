import unittest

from time import sleep
from os.path import dirname, abspath, join

from plyer.utils import platform
from plyer.facades.notification import Notification as NFacade
from plyer import notification


if platform == 'win':
    import ctypes
    from ctypes import (
        WINFUNCTYPE, POINTER,
        create_unicode_buffer,
        c_bool, c_int
    )
    from plyer.platforms.win.notification import WindowsNotification
    EnumWindows = ctypes.windll.user32.EnumWindows
    GetClassNameW = ctypes.windll.user32.GetClassNameW

elif platform == 'linux':
    from plyer.platforms.linux.notification import (
        NotifySendNotification,
        NotifyDbus
    )


class Test(unittest.TestCase):
    def show_notification(self, instance):
        path = dirname(abspath(__file__))
        instance.notify(
            title='title',
            message='My Message\nis multiline',
            app_name='Plyer Test',
            app_icon=join(path, 'images', 'kivy32.ico'),
            timeout=.1
        )

    def test_notification_windows(self):
        if platform != 'win':
            return

        # loop over windows and get refs to
        # the opened plyer notifications
        clsnames = []
        def fetch_class(hwnd, lParam):
            buff = create_unicode_buffer(50)
            GetClassNameW(hwnd, buff, 50)

            if 'Plyer' in buff.value:
                clsnames.append(buff.value)

        # ensure it's not an empty facade
        self.assertIsNot(notification, NFacade)
        self.assertIsInstance(notification, WindowsNotification)

        # create enum function for EnumWindows
        EnumWindowsProc = WINFUNCTYPE(
            # returns
            c_bool,

            # input params: hwnd, lParam
            POINTER(c_int), POINTER(c_int)
        )

        for i in range(3):
            self.show_notification(notification)

            # the balloon needs some time to became visible in WinAPI
            sleep(0.01)

            # fetch window class names
            EnumWindows(
                # enum & params
                EnumWindowsProc(fetch_class), None
            )

            # 3 active balloons at the same time,
            # class_name is incremented - see WindowsBalloonTip
            self.assertEqual(len(clsnames), i + 1)
            self.assertIn('PlyerTaskbar' + str(i), clsnames)
            clsnames = []

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
