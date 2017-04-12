'''
Android SMS
-----------
'''


from jnius import autoclass
from plyer.facades import Sms
from plyer.platforms.android import activity

Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')


class AndroidSms(Sms):

    def _send(self, **kwargs):
        '''
        This method provides sending messages to recipients.

        Expects 2 parameters in kwargs:
            - recipient: String type
            - message: String type

        Opens a mesage interface with recipient and message information.
        '''
        recipient = kwargs.get('recipient')
        message = kwargs.get('message')

        uri = Uri.parse('sms:' + str(recipient))
        intent = Intent(Intent.ACTION_VIEW, uri)

        if message:
            #not yet supported by android
            pass

        activity.startActivity(intent)


def instance():
    return AndroidSms()
