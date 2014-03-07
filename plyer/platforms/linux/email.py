from plyer.facades import Email
import webbrowser


class LinuxEmail(Email):
    def _send(self, **kwargs):
        recipient = kwargs.get('recipient')
        subject = kwargs.get('subject')
        text = kwargs.get('text')

        if recipient is None:
            recipient = ''
        if subject is None:
            subject = ''

        email_strings = ['mailto:{}'.format(recipient)]
        if subject or text:
            email_strings.append('?')
        if subject:
            email_strings.append('subject={}'.format(subject))
        if text:
            email_strings.append('&body={}'.format(text))

        webbrowser.open(''.join(email_strings))
            

def instance():
    return LinuxEmail()
