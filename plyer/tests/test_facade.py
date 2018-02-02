import unittest

import sys
import plyer
from os.path import join


# dummy pyjnius class to silence the import + config
class DummyJnius(object):
    def __init__(self, *args, **kwargs):
        class JavaClass:
            def __init__(self):
                self.ANDROID_VERSION = None
                self.SDK_INT = 1
                self.mActivity = None

        self.autoclass = lambda *a, **kw: JavaClass()


class FacadeTestCase(unittest.TestCase):
    def test_facade_android(self):
        plyer.utils.platform = 'android'

        # android platform automatically imports jnius
        sys.modules['jnius'] = DummyJnius()
        Proxy = plyer.utils.Proxy
        dummy = Proxy('dummy', plyer.facades.Dummy)

        self.assertEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__,
            plyer.platforms.android.dummy.AndroidDummy
        )
        self.assertIsInstance(
            dummy.show(),
            plyer.platforms.android.dummy.AndroidDummy
        )

    def test_facade_ios(self):
        plyer.utils.platform = 'ios'
        Proxy = plyer.utils.Proxy
        dummy = Proxy('dummy', plyer.facades.Dummy)

        self.assertEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__,
            plyer.platforms.ios.dummy.IosDummy
        )
        self.assertIsInstance(
            dummy.show(),
            plyer.platforms.ios.dummy.IosDummy
        )

    def test_facade_windows(self):
        plyer.utils.platform = 'win'
        Proxy = plyer.utils.Proxy
        dummy = Proxy('dummy', plyer.facades.Dummy)

        self.assertEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__,
            plyer.platforms.win.dummy.WinDummy
        )
        self.assertIsInstance(
            dummy.show(),
            plyer.platforms.win.dummy.WinDummy
        )

    def test_facade_osx(self):
        plyer.utils.platform = 'macosx'
        Proxy = plyer.utils.Proxy
        dummy = Proxy('dummy', plyer.facades.Dummy)

        self.assertEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__,
            plyer.platforms.macosx.dummy.MacosxDummy
        )
        self.assertIsInstance(
            dummy.show(),
            plyer.platforms.macosx.dummy.MacosxDummy
        )

    def test_facade_linux(self):
        plyer.utils.platform = 'linux'
        Proxy = plyer.utils.Proxy
        dummy = Proxy('dummy', plyer.facades.Dummy)

        self.assertEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__,
            plyer.platforms.linux.dummy.LinuxDummy
        )
        self.assertIsInstance(
            dummy.show(),
            plyer.platforms.linux.dummy.LinuxDummy
        )

    def test_facade_unknown(self):
        plyer.utils.platform = 'unknown'
        Proxy = plyer.utils.Proxy
        dummy = Proxy('dummy', plyer.facades.Dummy)

        # no 'unknown' platform (folder), fallback to facade
        self.assertNotEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__, plyer.facades.Dummy
        )
        with self.assertRaises(NotImplementedError):
            dummy.show()

    @classmethod
    def tearDownClass(cls):
        plyer.utils.platform = plyer.utils.Platform()


if __name__ == '__main__':
    unittest.main()
