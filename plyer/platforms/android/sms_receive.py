'''
Android Recieve SMS
-----------
'''

from jnius import autoclass
from plyer.facades import sms_receive
from jnius import PythonJavaClass
from jnius import java_method


Intent = autoclass('android.content.Intent')
Bundle = autoclass('android.os.Bundle')
GenericBroadcastReceiver = autoclass(
    'org.renpy.android.GenericBroadcastReceiver'
)
SmsMessage = autoclass('android.telephony.SmsMessage')
Toast = autoclass('android.widget.Toast')

class BroadcastReceiver(PythonJavaClass):
	__javainterfaces__ = [
	'org/renpy/android/GenericBroadcastReceiverCallback']
	__javacontext__ = 'app'

	def __init__(self, *args, **kwargs):
		PythonJavaClass.__init__(self, *args, **kwargs)
		

	@java_method(
		'(Landroid/content/Context;Landroid/content/Intent;)V')
	def onReceive(self, context, intent):
		bundle = intent.getExtras()
		messages = None
		string = ""
		if bundle:
			pdus = bundle.get('pdus')
			messages = SmsMessage[len(pdus)]
			for i in range(0, len(messages)):
				messages[i] = SmsMessage.createFromPdu(
					list(bytearray(pdus[i])))
				string += "Message from " + messages[i].getOriginatingAddress()
				string += " :"
				string += str(messages[i].getMessageBody())
				string += "\n"
			Toast.makeText(context, string, Toast.LENGTH_SHORT).show()

class AndroidReceiveSms(sms_receive):

	def _receive(self):
		return BroadcastReceiver()

def instance():
	return AndroidReceiveSms()
