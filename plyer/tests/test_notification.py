import unittest

import sys
import os.path as op

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)
from plyer import notification


class Test(unittest.TestCase):
    def test_notification(self):
        path = op.dirname(op.abspath(__file__))
        notification.notify(
            title='title',
            message='My Message\nis multiline',
            app_name='Plyer Test',
            app_icon=op.join(path, 'images', 'kivy32.ico'),
            timeout=3
        )


if __name__ == '__main__':
    unittest.main()
