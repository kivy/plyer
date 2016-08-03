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
        Label:
            text: 'Message'
        Label:
            text: root.sms_message
    BoxLayout:
        Label:
            text: 'Phone Number'
        Label:
            text: root.sms_phonenumber
''')


class SmsInterface(BoxLayout):
    sms_phonenumber = StringProperty()
    sms_message = StringProperty()

    def __init__(self, **kwargs):
        super(SmsInterface, self).__init__(**kwargs)
        try:
            self.sms_message = sms.message
            self.sms_phonenumber = str(sms.phonenumber)
        except:
            pass


class SmsApp(App):
    def build(self):
        return SmsInterface()

if __name__ == "__main__":
    SmsApp().run()
