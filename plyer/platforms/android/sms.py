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
PythonActivity = autoclass('org.renpy.android.PythonActivity')
GenericBroadcastReceiver = autoclass(
    'org.renpy.android.GenericBroadcastReceiver'
)
SmsManager = autoclass('android.telephony.SmsManager')
phoneNumbers = autoclass('android.opreference.PreferenceManager')


class AndroidSms(Sms):

    def _send(self, **kwargs):
        sms = SmsManager.getDefault()

        recipient = kwargs.get('recipient')
        message = kwargs.get('message')

        if sms:
            sms.sendTextMessage(recipient, None, message, None, None)

    class BroadcastReceiver(PythonJavaClass):
        '''Private class for receiving results from wifi manager.'''
        __javainterfaces__ = [
            'org/renpy/android/GenericBroadcastReceiverCallback'
        ]
        __javacontext__ = 'app'

        def __init__(self, facade, *args, **kwargs):
            PythonJavaClass.__init__(self, *args, **kwargs)
            self.facade = facade

        @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
        def onReceive(self, context, intent):
            phoneNumbers = PreferenceManager.getDefaultSharedPreferences(
                           context).getString("phone_entries", "")


def instance():
    return AndroidSms()
