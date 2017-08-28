import unittest

import sys
import os.path as op

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)
from plyer import uniqueid


class Test(unittest.TestCase):
    def test_uniqueid(self):
        self.assertTrue(len(uniqueid.id) > 0)


if __name__ == '__main__':
    unittest.main()
