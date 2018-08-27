'''
TestCPU
=======

Tested platforms:

* Windows
* Linux - nproc
'''

import unittest
from os import environ

from plyer.tests.common import PlatformTest, platform_import


class MockedNProc(object):
    '''
    Mocked object used instead of 'nproc' binary in the Linux specific API
    plyer.platforms.linux.cpu. The same output structure is tested for
    the range of <min_version, max_version>.

    .. note:: Extend the object with another data sample if it does not match.
    '''

    min_version = '8.21'
    max_version = '8.21'
    logical_cores = 99

    def __init__(self, *args, **kwargs):
        # only to ignore all args, kwargs
        pass

    @staticmethod
    def communicate():
        '''
        Mock Popen.communicate, so that 'nproc' isn't used.
        '''
        return (str(MockedNProc.logical_cores).encode('utf-8'), )

    @staticmethod
    def whereis_exe(binary):
        '''
        Mock whereis_exe, so that it looks like
        Linux NProc binary is present on the system.
        '''
        return binary == 'nproc'

    @staticmethod
    def logical():
        '''
        Return percentage from mocked data.
        '''
        return int(MockedNProc.logical_cores)


class TestCPU(unittest.TestCase):
    '''
    TestCase for plyer.cpu.
    '''

    @PlatformTest('linux')
    def test_cpu_linux_logical(self):
        '''
        Test mocked Linux NProc for plyer.cpu.
        '''
        cpu = platform_import(
            platform='linux',
            module_name='cpu',
            whereis_exe=MockedNProc.whereis_exe
        )
        cpu.Popen = MockedNProc
        cpu = cpu.instance()

        self.assertEqual(
            cpu.logical, MockedNProc.logical()
        )

    @PlatformTest('win')
    def test_cpu_win_logical(self):
        cpu = platform_import(
            platform='win',
            module_name='cpu'
        )

        cpu = cpu.instance()
        self.assertEqual(
            cpu.logical,
            # https://docs.microsoft.com/en-us/previous-versions/
            # windows/it-pro/windows-xp/bb490954(v=technet.10)
            int(environ['NUMBER_OF_PROCESSORS'])
        )


if __name__ == '__main__':
    unittest.main()
