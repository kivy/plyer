import unittest

import sys
import os.path as op

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)
from plyer import battery


class Test(unittest.TestCase):
    def test_battery(self):
        self.assertEqual(list(battery.status.keys()), ['isCharging', 'percentage'])


if __name__ == '__main__':
    unittest.main()
