'''
Android SMS
-----------
'''

from jnius import autoclass
from plyer.facades import Sms
from plyer.platform.android import require_permissions

SmsManager = autoclass('android.telephony.SmsManager')


class AndroidSms(Sms):

    @require_permissions("SEND_SMS")
    def _send(self, **kwargs):
        sms = SmsManager.getDefault()

        recipient = kwargs.get('recipient')
        message = kwargs.get('message')

        if sms:
            sms.sendTextMessage(recipient, None, message, None, None)


def instance():
    return AndroidSms()
