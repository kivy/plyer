'''
Module of Android API for plyer.email.
'''

from jnius import autoclass, cast  # pylint: disable=no-name-in-module
from plyer.facades import Email
from plyer.platforms.android import activity

INTENT = autoclass('android.content.Intent')
ANDROIDSTRING = autoclass('java.lang.String')


class AndroidEmail(Email):
    # pylint: disable=too-few-public-methods
    '''
    Implementation of Android email API.
    '''

    def _send(self, **kwargs):
        intent = INTENT(INTENT.ACTION_SEND)
        intent.setType('text/plain')

        recipient = kwargs.get('recipient')
        subject = kwargs.get('subject')
        text = kwargs.get('text')
        create_chooser = kwargs.get('create_chooser')

        if recipient:
            intent.putExtra(INTENT.EXTRA_EMAIL, [recipient])
        if subject:
            android_subject = cast('java.lang.CharSequence',
                                   ANDROIDSTRING(subject))
            intent.putExtra(INTENT.EXTRA_SUBJECT, android_subject)
        if text:
            android_text = cast('java.lang.CharSequence',
                                ANDROIDSTRING(text))
            intent.putExtra(INTENT.EXTRA_TEXT, android_text)

        if create_chooser:
            chooser_title = cast('java.lang.CharSequence',
                                 ANDROIDSTRING('Send message with:'))
            activity.startActivity(
                INTENT.createChooser(intent, chooser_title)
            )
        else:
            activity.startActivity(intent)


def instance():
    '''
    Instance for facade proxy.
    '''
    return AndroidEmail()
