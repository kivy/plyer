import subprocess
from urllib import quote
from plyer.facades import Email

class LinuxEmail(Email):
    def _send(self, **kwargs):
        recipient = kwargs.get('recipient')
        subject = kwargs.get('subject')
        text = kwargs.get('text')
        create_chooser = kwargs.get('create_chooser')

        uri = "mailto:"
        args = ["xdg-email"]
        if recipient:
            uri += str(recipient)
            args += [str(recipient)]
        if subject:
            uri += "?" if not "?" in uri else "&"
            uri += "subject="
            uri += quote(str(subject))
            args += ["--subject", str(subject)]
        if text:
            uri += "?" if not "?" in uri else "&"
            uri += "body="
            uri += quote(str(text))
            args += ["--body", str(text)]

        try:
            subprocess.Popen(args)
        except OSError:
            try:
                subprocess.Popen(["xdg-open", uri])
            except OSError:
                print "Warning: unable to start an email client. Make sure xdg-open is installed."


def instance():
    return LinuxEmail()
