'''
TestAudio
=========

Tested platforms:

* macOS
* Windows

.. versionadded:: 1.3.3
'''

from __future__ import unicode_literals
import unittest
import time

from os import mkdir, remove, environ
from os.path import join, expanduser, exists
from plyer.tests.common import platform_import, PlatformTest


class TestAudio(unittest.TestCase):
    '''
    TestCase for plyer.audio.

    .. versionadded:: 1.3.3
    '''

    @PlatformTest('macosx')
    def test_audio_macosx(self):
        '''
        Test macOS audio start, stop and play

        .. versionadded:: 1.3.3
        '''

        path = join(expanduser('~'), 'Music')
        if not exists(path):
            mkdir(path)

        audio = platform_import(
            platform='macosx',
            module_name='audio',
        )

        self.assertIn('OSXAudio', dir(audio))
        audio = audio.instance()
        self.assertIn('OSXAudio', str(audio))

        self.assertFalse(exists(audio.file_path))
        self.assertIsNone(audio.start())
        time.sleep(0.5)
        self.assertIsNone(audio.stop())
        self.assertIsNone(audio.play())
        time.sleep(0.5)
        self.assertIsNone(audio.stop())

        audio.file_path = audio.file_path.replace(
            'file://', ''
        )

        self.assertTrue(exists(audio.file_path))

        remove(audio.file_path)

    @PlatformTest('win')
    def test_audio_win(self):
        '''
        Test Windows audio start, stop and play

        .. versionadded:: 1.3.3
        '''

        path = join(environ['USERPROFILE'], 'Music')
        if not exists(path):
            mkdir(path)

        audio = platform_import(
            platform='win',
            module_name='audio',
        )

        self.assertIn('WinAudio', dir(audio))
        audio = audio.instance()
        self.assertIn('WinAudio', str(audio))

        self.assertFalse(exists(audio.file_path))
        self.assertIsNone(audio.start())
        time.sleep(0.5)
        self.assertIsNone(audio.stop())
        self.assertIsNone(audio.play())
        time.sleep(0.5)
        self.assertIsNone(audio.stop())

        self.assertTrue(exists(audio.file_path))

        remove(audio.file_path)


if __name__ == '__main__':
    unittest.main()
