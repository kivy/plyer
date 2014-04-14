'''
Android SMS
-----------
'''

from jnius import autoclass
from plyer.facades import Sms

SmsManager = autoclass('android.telephony.SmsManager')
class AndroidSms(Sms):

    def _send(self, **kwargs):
        sms = SmsManager.getDefault()

        phone_number = kwargs.get('phone_number')
        message = kwargs.get('message')

        if sms:
            sms.sendTextMessage(phone_number, None, message, None, None)

def instance():
    return AndroidSms()
