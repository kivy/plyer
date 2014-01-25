from jnius import autoclass, cast
from plyer.facades import Email
from plyer.platforms.android import activity

Intent = autoclass('android.content.Intent')
AndroidString = autoclass('java.lang.String')
Uri = autoclass('android.net.Uri')

class AndroidEmail(Email):
    def _send(self, **kwargs):
        print 'Using ANDROIDEMAIL'
        intent = Intent(Intent.ACTION_SEND)
        intent.setType('text/plain')

        recipient = kwargs.get('recipient')
        subject = kwargs.get('subject')
        text = kwargs.get('text')
        attachment = kwargs.get('attachment')

        if recipient:
            android_recipient = cast('java.lang.CharSequence',
                                     AndroidString(recipient))
            intent.putExtra(Intent.EXTRA_EMAIL, android_recipient)
        if subject:
            android_subject = cast('java.lang.CharSequence',
                                   AndroidString(subject))
            intent.putExtra(Intent.EXTRA_SUBJECT, android_subject)
        if text:
            android_text = cast('java.lang.CharSequence',
                                AndroidString(android_text))
            intent.putExtra(Intent.EXTRA_TEXT, android_text)
        if attachment:
            android_attachment = AndroidString('file://' + attachment))
            intent.putExtra(Intent.EXTRA_STREAM, Uri.parse(android_attachment))

        activity.startActivity(intent)


def instance():
    return AndroidEmail()
