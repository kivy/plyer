'''
Android SMS
-----------
'''

from jnius import autoclass
from plyer.facades import Sms
from . import activity

SmsManager = autoclass('android.telephony.SmsManager')

Intent = autoclass('android.content.Intent')
uri = autoclass('android.net.Uri')

class AndroidSms(Sms):

    def _send(self, **kwargs):
        sms = SmsManager.getDefault()

        recipient = kwargs.get('recipient')
        message = kwargs.get('message')

        if sms:
            sms.sendTextMessage(recipient, None, message, None, None)

    def _edit(self, **kwargs):
        recipient = kwargs.get('recipient')
        address = recipient or ""
        message = kwargs.get('message')
        sms_body = message or ""

        if not address:
            intent = Intent(Intent.ACTION_SEND)
            intent.setType("text/plain")
            intent.putExtra(Intent.EXTRA_TEXT, sms_body)
            package = autoclass(
                'android.provider.Telephony.Sms').getDefaultSmsPackage()
            if package:
                intent.setPackage(package)
        else:
            intent = Intent(Intent.ACTION_SENDTO)
            intent.setData(uri.parse("smsto:" + uri.encode(address)))
            intent.putExtra("sms_body", sms_body)

        activity.startActivity(intent)


def instance():
    return AndroidSms()
