'''
TestScreenshot
==============

Tested platforms:

* MacOS
'''

import unittest

from os import mkdir, remove
from os.path import join, expanduser, exists

from mock import patch
from plyer.compat import PY2
from plyer.tests.common import PlatformTest, platform_import


class MockedScreenCapture(object):
    '''
    Mocked object used instead of the console-like calling
    of screencapture binary with parameters.
    '''
    @staticmethod
    def whereis_exe(binary):
        '''
        Mock whereis_exe, so that it looks like
        MacOS screencapture binary is present on the system.
        '''
        return binary == 'screencapture'

    @staticmethod
    def call(args):
        '''
        Mocked subprocess.call to check console parameters.
        '''
        assert len(args) == 2, len(args)
        assert args[0] == 'screencapture', args
        assert args[1] == join(
            expanduser('~'), 'Pictures', 'screenshot.png'
        ), args
        with open(args[1], 'w') as scr:
            scr.write('')


class TestScreenshot(unittest.TestCase):
    '''
    TestCase for plyer.screenshot.
    '''

    def setUp(self):
        path = join(expanduser('~'), 'Pictures')
        if not exists(path):
            mkdir(path)

    @PlatformTest('macosx')
    def test_screenshot_screencapture(self):
        '''
        Test mocked MacOS screencapture for plyer.screenshot.
        '''
        if not PY2:
            print('Can not run until PyOBJus works on Py3.')
            return

        scr = platform_import(
            platform='macosx',
            module_name='screenshot',
            whereis_exe=MockedScreenCapture.whereis_exe
        )

        # such class exists in screenshot module
        self.assertIn('OSXScreenshot', dir(scr))

        # the required instance is created
        scr = scr.instance()
        self.assertIn('OSXScreenshot', str(scr))

        # move capture from context manager to run without mock
        with patch(target='subprocess.call', new=MockedScreenCapture.call):
            self.assertIsNone(scr.capture())

        scr_path = join(
            expanduser('~'), 'Pictures', 'screenshot.png'
        )
        self.assertTrue(exists(scr_path))
        remove(scr_path)


if __name__ == '__main__':
    unittest.main()
