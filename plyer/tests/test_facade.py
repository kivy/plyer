'''
TestFacade
==========

Tested platforms:

* Android
* iOS
* Windows
* MacOS
* Linux
'''

import unittest

import sys
from copy import copy
from os import remove
from os.path import abspath, dirname, join

from mock import Mock

import plyer
from plyer.tests.common import reload


# dummy pyjnius class to silence the import + config
class DummyJnius(object):
    '''
    Mocked PyJNIus module.
    '''

    # pylint: disable=too-few-public-methods
    def __init__(self, *args, **kwargs):
        # pylint: disable=unused-argument
        class JavaClass:
            '''
            Mocked PyJNIus JavaClass object.
            '''

            def __init__(self):
                # pylint: disable=invalid-name
                self.ANDROID_VERSION = None
                self.SDK_INT = 1
                self.mActivity = None

        self.autoclass = lambda *a, **kw: JavaClass()


class TestFacade(unittest.TestCase):
    '''
    TestCase for plyer.utils.Proxy and plyer.facades.
    '''

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
        with open(join(fac_path, 'dummy.py'), 'w') as fle:
            fle.write(dummy_facade)

        # create Dummy platform modules
        for plat in {'android', 'ios', 'win', 'macosx', 'linux'}:
            with open(join(plat_path, plat, 'dummy.py'), 'w') as fle:
                fle.write(dummy.format(
                    **{'plat': plat.title()}
                ))

        # make Dummy facade available in plyer
        injected = False
        with open(join(fac_path, '__init__.py'), 'r+') as fle:

            # make a backup of original file
            facades_old = fle.readlines()

            # return to the beginning of a file and inject
            fle.seek(0)
            for line in facades_old:
                # inject before the first importing (necessary for __all__)
                if line.startswith('from ') or line.startswith('import '):
                    # if injected and on an import line,
                    # proceed with default
                    if injected:
                        fle.write(line)
                        continue

                    # injecting Dummy facade to plyer
                    fle.write(
                        '\nfrom plyer.facades.dummy import Dummy\n'
                        '__all__ += ("Dummy", )\n'
                    )
                    injected = True

                # write line by default
                fle.write(line)
            fle.truncate()

        with open(join(fac_path, '__old_init__.py'), 'w') as fle:
            fle.write(''.join(facades_old))

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
        '''
        Test for returning an object for Android API implementation
        from Proxy object using a dynamically generated dummy objects.
        '''

        plyer.utils.platform = 'android'

        # android platform automatically imports jnius
        sys.modules['jnius'] = DummyJnius()
        proxy_cls = plyer.utils.Proxy
        dummy = proxy_cls(
            'dummy', plyer.facades.Dummy  # pylint: disable=no-member
        )

        self.assertEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__,
            # pylint: disable=no-member
            plyer.platforms.android.dummy.AndroidDummy
        )
        self.assertIsInstance(
            dummy.show(),
            # pylint: disable=no-member
            plyer.platforms.android.dummy.AndroidDummy
        )

    def test_facade_ios(self):
        '''
        Test for returning an object for iOS API implementation
        from Proxy object using a dynamically generated dummy objects.
        '''

        plyer.utils.platform = 'ios'
        proxy_cls = plyer.utils.Proxy
        dummy = proxy_cls(
            'dummy', plyer.facades.Dummy  # pylint: disable=no-member
        )

        self.assertEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__,
            plyer.platforms.ios.dummy.IosDummy  # pylint: disable=no-member
        )
        self.assertIsInstance(
            dummy.show(),
            plyer.platforms.ios.dummy.IosDummy  # pylint: disable=no-member
        )

    def test_facade_windows(self):
        '''
        Test for returning an object for Windows API implementation
        from Proxy object using a dynamically generated dummy objects.
        '''

        plyer.utils.platform = 'win'
        proxy_cls = plyer.utils.Proxy
        dummy = proxy_cls(
            'dummy', plyer.facades.Dummy  # pylint: disable=no-member
        )

        self.assertEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__,
            plyer.platforms.win.dummy.WinDummy  # pylint: disable=no-member
        )
        self.assertIsInstance(
            dummy.show(),
            plyer.platforms.win.dummy.WinDummy  # pylint: disable=no-member
        )

    def test_facade_osx(self):
        '''
        Test for returning an object for MacOS API implementation
        from Proxy object using a dynamically generated dummy objects.
        '''

        plyer.utils.platform = 'macosx'
        proxy_cls = plyer.utils.Proxy
        dummy = proxy_cls(
            'dummy', plyer.facades.Dummy  # pylint: disable=no-member
        )

        self.assertEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__,
            # pylint: disable=no-member
            plyer.platforms.macosx.dummy.MacosxDummy
        )
        self.assertIsInstance(
            dummy.show(),
            # pylint: disable=no-member
            plyer.platforms.macosx.dummy.MacosxDummy
        )

    def test_facade_linux(self):
        '''
        Test for returning an object for Linux API implementation
        from Proxy object using a dynamically generated dummy objects.
        '''

        plyer.utils.platform = 'linux'
        proxy_cls = plyer.utils.Proxy
        dummy = proxy_cls(
            'dummy', plyer.facades.Dummy  # pylint: disable=no-member
        )

        self.assertEqual(
            str(dummy), plyer.utils.platform
        )
        self.assertEqual(
            dummy.__class__,
            plyer.platforms.linux.dummy.LinuxDummy  # pylint: disable=no-member
        )
        self.assertIsInstance(
            dummy.show(),
            plyer.platforms.linux.dummy.LinuxDummy  # pylint: disable=no-member
        )

    def test_facade_unknown(self):
        '''
        Test fallback of Proxy to facade if there
        is no such requested platform.
        '''

        plyer.utils.platform = 'unknown'

        # no 'unknown' platform (folder), fallback to facade
        class MockedProxy(plyer.utils.Proxy):
            # pylint: disable=too-few-public-methods
            '''
            Partially mocked Proxy class, so that we pull the error
            from traceback.print_exc to the test and check the calls.
            '''

            # _ensure_obj is called only once, to either
            # get the platform object or fall back to facade
            # therefore the three self.asserts below will return
            # different values
            expected_asserts = [True, False, False]

            def _ensure_obj(inst):
                # pylint: disable=no-self-argument
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

        proxy_cls = MockedProxy
        dummy = proxy_cls(
            'dummy', plyer.facades.Dummy  # pylint: disable=no-member
        )

        self.assertNotEqual(
            str(dummy), plyer.utils.platform
        )

        self.assertEqual(
            dummy.__class__, plyer.facades.Dummy  # pylint: disable=no-member
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

        with open(join(fac_path, '__old_init__.py')) as fle:
            facades_old = fle.read()
        remove(join(fac_path, '__old_init__.py'))

        # restore the original facades __init__.py
        with open(join(fac_path, '__init__.py'), 'w') as fle:
            fle.write(''.join(facades_old))
        plyer.utils.platform = plyer.utils.Platform()


if __name__ == '__main__':
    unittest.main()
