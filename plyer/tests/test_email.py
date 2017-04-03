import unittest

import sys
import os.path as op

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)
from plyer.platforms.win import email
from plyer.utils import platform


class Test(unittest.TestCase):
    def test_email_win(self):
        if platform != 'win':
            return

        # replace os.startfile to compare final value
        _startfile = globals()['email'].__dict__['os'].startfile

        # instead of os.startfile create a variable to compare
        globals()['email'].__dict__['os'].startfile = lambda *args: setattr(
            self, 'mailto', args[0]
        )

        try:
            test_mailto = 'mailto:recipient?subject=subject&body=text'
            email.WindowsEmail().send(
                recipient='recipient',
                subject='subject',
                text='text'
            )
            self.assertEqual(self.mailto, test_mailto)
        except WindowsError:
            # if WE is raised, email client isn't found,
            # but the platform code works correctly
            print('Mail client not found!')

        # give back startfile and remove mailto
        globals()['email'].__dict__['os'].startfile = _startfile
        del self.mailto


if __name__ == '__main__':
    unittest.main()
