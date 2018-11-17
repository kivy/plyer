'''
TestAudio
=========

Tested platforms:

* macOS
'''

import unittest
import time

from os import mkdir, remove
from os.path import join, expanduser, exists
from plyer.tests.common import platform_import, PlatformTest


class TestAudio(unittest.TestCase):
    '''
    TestCase for plyer.audio.
    '''

    @PlatformTest('macosx')
    def test_audio_macosx(self):
        '''
        Test macOS audio start, stop and play
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


if __name__ == '__main__':
    unittest.main()
