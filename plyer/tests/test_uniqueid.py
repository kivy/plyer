import unittest

from plyer import uniqueid


class Test(unittest.TestCase):
    def test_uniqueid(self):
        self.assertTrue(len(uniqueid.id) > 0)


if __name__ == '__main__':
    unittest.main()
