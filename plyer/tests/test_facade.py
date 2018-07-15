import unittest

import sys
import plyer
from copy import copy
from mock import Mock, patch
from os import mkdir, remove
from os.path import abspath, dirname, join

from plyer.tests.common import reload


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
    @classmethod
    def setUpClass(cls):
        # dummy files to test Proxy + facades
        dummy_facade = (
            'class Dummy(object):\n'
            '    def show(self):\n'
            '        raise NotImplementedError()\n'
        )

        dummy = (
            'from plyer.facades import Dummy\n\n\n'
            'class {plat}Dummy(Dummy):\n'
            '    def show(self):\n'
            '        return self\n\n'
            '    def __str__(self, *args):\n'
            '        return "{plat}".lower()\n\n\n'
            'def instance():\n'
            '    return {plat}Dummy()\n\n'
        )

        fac_path = join(
            dirname(dirname(abspath(__file__))),
            'facades'
        )
        plat_path = join(
            dirname(dirname(abspath(__file__))),
            'platforms'
        )

        # create Dummy facade
        with open(join(fac_path, 'dummy.py'), 'w') as f:
            f.write(dummy_facade)

        # create Dummy platform modules
        for plat in {'android', 'ios', 'win', 'macosx', 'linux'}:
            with open(join(plat_path, plat, 'dummy.py'), 'w') as f:
                f.write(dummy.format(
                    **{'plat': plat.title()}
                ))

        # make Dummy facade available in plyer
        injected = False
        with open(join(fac_path, '__init__.py'), 'r+') as f:

            # make a backup of original file
            facades_old = f.readlines()

            # return to the beginning of a file and inject
            f.seek(0)
            for line in facades_old:
                # inject before the first importing (necessary for __all__)
                if line.startswith('from ') or line.startswith('import '):
                    # if injected and on an import line,
                    # proceed with default
                    if injected:
                        f.write(line)
                        continue

                    # injecting Dummy facade to plyer
                    f.write(
                        '\nfrom plyer.facades.dummy import Dummy\n'
                        '__all__ += ("Dummy", )\n'
                    )
                    injected = True

                # write line by default
                f.write(line)
            f.truncate()

        with open(join(fac_path, '__old_init__.py'), 'w') as f:
            f.write(''.join(facades_old))

        # reload everything from plyer
        # (and other modules if necessary)
        module_cls = type(sys)
        include = {'plyer'}
        for key, val in copy(sys.modules).items():
            if any([pattern not in key for pattern in include]):
                continue
            if any([pattern not in str(val) for pattern in include]):
                continue
            if not isinstance(val, module_cls):
                continue
            reload(val)

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

        # no 'unknown' platform (folder), fallback to facade
        class MockedProxy(plyer.utils.Proxy):
            # _ensure_obj is called only once, to either
            # get the platform object or fall back to facade
            # therefore the three self.asserts below will return
            # different values
            expected_asserts = [True, False, False]

            def _ensure_obj(inst):
                import sys
                # called once, prints to stderr

                # mock stderr because traceback.print_exc uses it
                # https://github.com/python/cpython/blob/
                # 16dfca4d829e45f36e71bf43f83226659ce49315/Lib/traceback.py#L99
                sys.stderr = Mock()

                # call the original function to trigger
                # ImportError warnings in stderr
                super(MockedProxy, inst)._ensure_obj()

                # Traceback (most recent call last):
                #   File "/app/plyer/utils.py", line 88, in _ensure_obj
                #     mod = __import__(module, fromlist='.')
                # ImportError: No module named unknown.dummy

                # must not use self.assertX
                # (has to be checked on the go!)
                expected_bool = MockedProxy.expected_asserts.pop(0)
                call_count = sys.stderr.write.call_count
                # 4 calls for py2, 6 calls for py3 with traceback.print_exc
                assert (call_count in (4, 6)) == expected_bool, call_count

                # return stderr to the original state
                sys.stderr = sys.__stderr__

        Proxy = MockedProxy
        dummy = Proxy('dummy', plyer.facades.Dummy)

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
        fac_path = join(
            dirname(dirname(abspath(__file__))),
            'facades'
        )
        plat_path = join(
            dirname(dirname(abspath(__file__))),
            'platforms'
        )

        # remove Dummy facade
        remove(join(fac_path, 'dummy.py'))

        # remove Dummy platform modules
        for plat in {'android', 'ios', 'win', 'macosx', 'linux'}:
            remove(join(plat_path, plat, 'dummy.py'))

        with open(join(fac_path, '__old_init__.py')) as f:
            facades_old = f.read()
        remove(join(fac_path, '__old_init__.py'))

        # restore the original facades __init__.py
        with open(join(fac_path, '__init__.py'), 'w') as f:
            f.write(''.join(facades_old))
        plyer.utils.platform = plyer.utils.Platform()


if __name__ == '__main__':
    unittest.main()
