'''
TestBattery
===========

Tested platforms:

* Windows
* Linux - upower
'''

import unittest

from plyer.compat import text_type
from plyer.tests.common import PlatformTest, platform_import


class MockedUPower(object):
    '''
    Mocked object used instead of 'upower' binary in the Linux specific API
    plyer.platforms.linux.battery. The same output structure is tested for
    the range of <min_version, max_version>.

    .. note:: Extend the object with another data sample if it does not match.
    '''

    min_version = '0.99.4'
    max_version = '0.99.4'

    values = {
        u'Device': u'/org/freedesktop/UPower/devices/battery_BAT0',
        u'native-path': u'BAT0',
        u'vendor': u'ASUS',
        u'model': u'1005HA',
        u'power supply': u'yes',
        u'updated': u'Thu 05 Jul 2018 23:15:01 PM CEST',
        u'has history': u'yes',
        u'has statistics': u'yes',
        u'battery': {
            u'present': u'yes',
            u'rechargeable': u'yes',
            u'state': u'discharging',
            u'warning-level': u'none',
            u'energy': u'48,708 Wh',
            u'energy-empty': u'0 Wh',
            u'energy-full': u'54,216 Wh',
            u'energy-full-design': u'62,64 Wh',
            u'energy-rate': u'7,722 W',
            u'voltage': u'11,916 V',
            u'time to empty': u'6,3 hours',
            u'percentage': u'89%',
            u'capacity': u'86,5517%',
            u'technology': u'lithium-ion',
            u'icon-name': u"'battery-full-symbolic"
        },
        u'History (charge)': u'1530959637  89,000  discharging',
        u'History (rate)': u'1530958556  7,474   discharging'
    }

    data = text_type(
        '  native-path:          {native-path}\n'
        '  vendor:               {vendor}\n'
        '  model:                {model}\n'
        '  power supply:         {power supply}\n'
        '  updated:              {updated}\n'
        '  has history:          {has history}\n'
        '  has statistics:       {has statistics}\n'
        '  battery\n'
        '    present:              {battery[present]}\n'
        '    rechargeable:         {battery[rechargeable]}\n'
        '    state:                {battery[state]}\n'
        '    warning-level:        {battery[warning-level]}\n'
        '    energy:               {battery[energy]}\n'
        '    energy-empty:         {battery[energy-empty]}\n'
        '    energy-full:          {battery[energy-full]}\n'
        '    energy-full-design:   {battery[energy-full-design]}\n'
        '    energy-rate:          {battery[energy-rate]}\n'
        '    voltage:              {battery[voltage]}\n'
        '    time to empty:        {battery[time to empty]}\n'
        '    percentage:           {battery[percentage]}\n'
        '    capacity:             {battery[capacity]}\n'
        '    technology:           {battery[technology]}\n'
        '    icon-name:            {battery[icon-name]}\n'
        '  History (charge):\n'
        '    {History (charge)}\n'
        '  History (rate):\n'
        '    {History (rate)}\n'
    ).format(**values).encode('utf-8')
    # LinuxBattery calls decode()

    def __init__(self, *args, **kwargs):
        # only to ignore all args, kwargs
        pass

    @staticmethod
    def communicate():
        '''
        Mock Popen.communicate, so that 'upower' isn't used.
        '''
        return (MockedUPower.data, )

    @staticmethod
    def whereis_exe(binary):
        '''
        Mock whereis_exe, so that it looks like
        Linux UPower binary is present on the system.
        '''
        return binary == 'upower'

    @staticmethod
    def charging():
        '''
        Return charging bool from mocked data.
        '''
        return MockedUPower.values['battery']['state'] == 'charging'

    @staticmethod
    def percentage():
        '''
        Return percentage from mocked data.
        '''
        percentage = MockedUPower.values['battery']['percentage'][:-1]
        return float(percentage.replace(',', '.'))


class TestBattery(unittest.TestCase):
    '''
    TestCase for plyer.battery.
    '''

    def test_battery_linux_upower(self):
        '''
        Test mocked Linux UPower for plyer.battery.
        '''
        battery = platform_import(
            platform='linux',
            module_name='battery',
            whereis_exe=MockedUPower.whereis_exe
        )
        battery.Popen = MockedUPower
        battery = battery.instance()

        self.assertEqual(
            battery.status, {
                'isCharging': MockedUPower.charging(),
                'percentage': MockedUPower.percentage()
            }
        )

    @PlatformTest('win')
    def test_battery_win(self):
        '''
        Test Windows API for plyer.battery.
        '''
        battery = platform_import(
            platform='win',
            module_name='battery'
        ).instance()
        for key in ('isCharging', 'percentage'):
            self.assertIn(key, battery.status)
            self.assertIsNotNone(battery.status[key])


if __name__ == '__main__':
    unittest.main()
