from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty

from plyer import sms

Builder.load_string('''
<SmsInterface>:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: sp(30)
        Label:
            text: 'Recipient:'
        TextInput:
            id: recipient
            multiline: False
            on_text_validate: message.focus = True
    BoxLayout:
        Label:
            text: 'Message:'
        TextInput:
            id: message
    IntentButton:
        sms_recipient: recipient.text
        sms_message: message.text
        text: 'Send SMS'
        size_hint_y: None
        height: sp(40)
        on_release: self.send_sms()
''')


class SmsInterface(BoxLayout):
    pass


class IntentButton(Button):
    sms_recipient = StringProperty()
    sms_message = StringProperty()

    def send_sms(self, *args):
        sms.send(recipient=self.sms_recipient, message=self.sms_message)


class SmsApp(App):
    def build(self):
        return SmsInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    SmsApp().run()
