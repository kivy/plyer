'''
TestDeviceName
============

Tested platforms:

* Windows
'''

import unittest
from mock import patch, Mock
from plyer.tests.common import PlatformTest, platform_import
import socket


class TestDeviceName(unittest.TestCase):
    '''
    TestCase for plyer.devicename.
    '''

    def test_devicename(self):
        '''
        General all platform test for plyer.devicename.
        '''
        from plyer import devicename
        self.assertTrue(len(devicename.device_name) > 0)

    @PlatformTest('win')
    def test_devicename_win(self):
        '''
        Test Windows API for plyer.devicename.
        '''
        devicename = platform_import(
            platform='Win',
            module_name='devicename',
        )
        with patch.object(socket,
                          'gethostname',
                          return_value='mocked_hostname'
                          ) as mock_method:
            evaluated_device_name = devicename.device_name
            self.assertEqual(evaluated_device_name, 'mocked_hostname')


if __name__ == '__main__':
    unittest.main()
