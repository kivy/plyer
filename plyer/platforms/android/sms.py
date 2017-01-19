'''
Android SMS
-----------
'''

from jnius import autoclass
from jnius import cast
from plyer.facades import Sms

PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')


class AndroidSms(Sms):

    def _send(self, **kwargs):
        recipient = kwargs.get('recipient')
        message = kwargs.get('message')

        sendIntent = Intent()
        sendIntent.setAction(Intent.ACTION_VIEW)
        sendIntent.setType('vnd.android-dir/mms-sms')
        sendIntent.putExtra('address', recipient)
        sendIntent.putExtra('sms_body', message)

        currentActivity = cast(
                                'android.app.Activity',
                                PythonActivity.mActivity)
        currentActivity.startActivity(sendIntent)


def instance():
    return AndroidSms()
