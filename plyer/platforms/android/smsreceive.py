'''
Android Receive SMS
-----------
'''

from jnius import autoclass
from plyer.facades import SmsReceive
from jnius import PythonJavaClass
from jnius import java_method


Intent = autoclass('android.content.Intent')
Bundle = autoclass('android.os.Bundle')
GenericBroadcastReceiver = autoclass(
    'org.renpy.android.GenericBroadcastReceiver')
SmsMessage = autoclass('android.telephony.SmsMessage')
Toast = autoclass('android.widget.Toast')


class BroadcastReceiver(PythonJavaClass):
    __javainterfaces__ = [
        'org/renpy/android/GenericBroadcastReceiverCallback']

    __javacontext__ = 'app'

    def __init__(self, *args, **kwargs):
        super(BroadcastReceiver, self).__init__(self, *args, **kwargs)

    @java_method(
        '(Landroid/content/Context;Landroid/content/Intent;)V')
    def onReceive(self, context, intent):

        bundle = intent.getExtras()
        messages = None
        string = ""
        if not bundle:
            raise ReceiveError()
        else:
            pdus = bundle.get('pdus')
            messages = SmsMessage[len(pdus)]
            for i in range(len(messages)):
                messages[i] = SmsMessage.createFromPdu(
                    list(bytearray(pdus[i])))
                string += "Message from " +\
                    messages[i].getOriginatingAddress() +\
                    " :" + str(messages[i].getMessageBody()) + "\n"
            Toast.makeText(context, string, Toast.LENGTH_SHORT).show()


class AndroidReceiveSms(SmsReceive):

    def _startreceiver(self):
        return BroadcastReceiver()


def instance():
    return AndroidReceiveSms()
