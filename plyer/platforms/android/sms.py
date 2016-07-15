'''
Android SMS
-----------
'''

from jnius import autoclass
from plyer.facades import Sms
from jnius import autoclass, cast
from plyer.facades import Sharing
from plyer.platforms.android import activity
from jnius import PythonJavaClass
from jnius import java_method


Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')
IntentFilter = autoclass('android.content.IntentFilter')
uri = autoclass('android.net.Uri')
Bundle = autoclass('android.os.Bundle')
PythonActivity = autoclass('org.renpy.android.PythonActivity')
GenericBroadcastReceiver = autoclass(
    'org.renpy.android.GenericBroadcastReceiver'
)
SmsMessage = autoclass('android.telephony.SmsMessage')
SmsManager = autoclass('android.telephony.SmsManager')


class AndroidSms(Sms):
    phonenumber = None
    msgreceived = None

    def _send(self, **kwargs):
        sms = SmsManager.getDefault()

        recipient = kwargs.get('recipient')
        message = kwargs.get('message')

        if sms:
            sms.sendTextMessage(recipient, None, message, None, None)

    class BroadcastReceiver(PythonJavaClass):
        '''Private class for receiving results from Sms manager.'''
        __javainterfaces__ = [
            'org/renpy/android/GenericBroadcastReceiverCallback'
        ]
        __javacontext__ = 'app'

        def __init__(self, facade, *args, **kwargs):
            PythonJavaClass.__init__(self, *args, **kwargs)
            self.facade = facade

        @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
        def onReceive(self, context, intent):
            try:
                Bundle = intent.getExtras()
                _msgreceived = ''
                if Bundle:
                    # array of objects.
                    pdus = Bundle.get('pdus')
                    # SmsMessage is an array.
                    msg = SmsMessage(len(pdus))
                    for i in range(len(pdus)):
                        msg[i] = SmsMessage.createFromPdu(pdus[i])
                        _msgreceived += msg[i].getMessageBody().toString()
                        _msgreceived += '\n'
                        _phonenumber = msg[0].getOriginatingAddress()
                        self.facade.phonenumber = _phonenumber
                        self.facade.msgreceived = _msgreceived
            except:
                import traceback
                traceback.print_exc()

    def _get_message(self):
        return "sdfsdfsd"
        return self.msgreceived

    def _get_phonenumber(self):
        return self.phonenumber


def instance():
    return AndroidSms()
