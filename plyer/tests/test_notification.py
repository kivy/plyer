'''
TestNotification
================

Tested platforms:

* Linux - notify-send
'''

import unittest
import mock

from time import sleep
from os.path import dirname, abspath, join

from plyer.utils import platform
from plyer.tests.common import PlatformTest, platform_import


class MockedNotifySend(object):
    @staticmethod
    def whereis_exe(binary):
        return binary == 'notify-send'

    @staticmethod
    def call(args):
        assert len(args) >= 3
        assert TestNotification.data['title'] in args
        assert TestNotification.data['message'] in args

    @staticmethod
    def warn(msg):
        assert 'dbus package is not installed' in msg


class TestNotification(unittest.TestCase):
    data = {
        'title': 'title',
        'message': 'My Message\nis multiline',
        'app_name': 'Plyer Test',
        'app_icon': join(
            dirname(abspath(__file__)),
            'images', 'kivy32.ico'
        ),
        'timeout': 0.1
    }

    def show_notification(self, instance):
        instance.notify(**self.data)

    @PlatformTest('win')
    def test_notification_windows(self):

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

    @PlatformTest('linux')
    def test_notification_notifysend(self):
        notif = platform_import(
            platform='linux',
            module_name='notification',
            whereis_exe=MockedNotifySend.whereis_exe
        )
        self.assertIn('NotifySendNotification', dir(notif))
        with mock.patch(target='warnings.warn', new=MockedNotifySend.warn):
            notif = notif.instance()
        self.assertIn('NotifySendNotification', str(notif))

        with mock.patch(target='subprocess.call', new=MockedNotifySend.call):
            self.assertIsNone(self.show_notification(notif))


if __name__ == '__main__':
    unittest.main()
