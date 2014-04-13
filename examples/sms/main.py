from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty

from plyer import sms

Builder.load_string('''
#:import sms plyer.sms
<SmsInterface>:
    orientation: 'vertical'
    BoxLayout:
        Label:
            text: 'Phone number:'
        TextInput:
            id: phone_number
    BoxLayout:
        Label:
            text: 'Message:'
        TextInput:
            id: message
    IntentButton:
        phone_num: phone_number.text
        msg: message.text
        text: 'Send Sms'
        on_release: self.send_sms()
''')


class SmsInterface(BoxLayout):
    pass

class IntentButton(Button):
    phone_num = StringProperty()
    msg = StringProperty()

    def send_sms(self, *args):
        sms.send(phone_number=self.phone_num,
                   message=self.msg)

class SmsApp(App):
    def build(self):
        return SmsInterface()

if __name__ == "__main__":
    SmsApp().run()
