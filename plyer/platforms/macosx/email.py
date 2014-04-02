import subprocess
from urllib import quote
from plyer.facades import Email

class OSXEmail(Email):
    def _send(self, **kwargs):
        recipient = kwargs.get('recipient')
        subject = kwargs.get('subject')
        text = kwargs.get('text')
        create_chooser = kwargs.get('create_chooser')

        uri = "mailto:"
        if recipient:
            uri += str(recipient)
        if subject:
            uri += "?" if not "?" in uri else "&"
            uri += "subject="
            uri += quote(str(subject))
        if text:
            uri += "?" if not "?" in uri else "&"
            uri += "body="
            uri += quote(str(text))

        subprocess.Popen(["open", uri])


def instance():
    return OSXEmail()

