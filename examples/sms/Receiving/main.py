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
            text: 'Title'
        Label:
            text: "Message"
    Label:
        text: 'From'
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

if __name__ == "__main__":
    SmsApp().run()
