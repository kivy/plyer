
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty

from plyer import email

Builder.load_string('''
<EmailInterface>:
    orientation: 'vertical'
    BoxLayout:
        Label:
            text: 'Recipient:'
        TextInput:
            id: recipient
    BoxLayout:
        Label:
            text: 'Subject:'
        TextInput:
            id: subject
    BoxLayout:
        Label:
            text: 'text'
        TextInput:
            id: text
    BoxLayout:
        Label:
            text: 'create chooser?'
        CheckBox:
            id: create_chooser
    IntentButton:
        email_recipient: recipient.text
        email_subject: subject.text
        email_text: text.text
        create_chooser: create_chooser.active
        text: 'Send email'
        size_hint_y: None
        height: sp(40)
        on_release: self.send_email()
''')


class EmailInterface(BoxLayout):
    pass


class IntentButton(Button):
    email_recipient = StringProperty()
    email_subject = StringProperty()
    email_text = StringProperty()
    create_chooser = BooleanProperty()

    def send_email(self, *args):
        email.send(recipient=self.email_recipient,
                   subject=self.email_subject,
                   text=self.email_text,
                   create_chooser=self.create_chooser)


class EmailApp(App):
    def build(self):
        return EmailInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    EmailApp().run()
