from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty
from plyer import call
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Builder.load_string('''
#: import Platform kivy.utils.platform
<CallInterface>:
    orientation: 'vertical'
    Label:
    BoxLayout:
        size_hint_y: None
        size: (400,100)
        TextInput:
            id: number
            hint_text: "Enter Number"
            multiline: False
        MakeCallButton:
            tel: number.text
            text: 'Make call via this app'
            on_release: self.call()
    Label:
        text: "OR"
    DialCallButton:
        size_hint_y: None
        size: (400,100)
        disabled: True if Platform == 'ios' else False
        text: "Dial call via  phone"
        on_release: self.dial()
    Label:

<ErrorPopup>:
    title: "Error!"
    size_hint: .5, .5
    Label:
        text: "Feature not available for this platform !"

''')


class CallInterface(BoxLayout):
    pass


class ErrorPopup(Popup):
    pass


class DialCallButton(Button):

    def dial(self, *args):
        try:
            call.dialcall()
        except NotImplementedError:
            popup = ErrorPopup()
            popup.open()


class MakeCallButton(Button):
    tel = StringProperty()

    def call(self, *args):
        try:
            call.makecall(tel=self.tel)
        except NotImplementedError:
            popup = ErrorPopup()
            popup.open()


class CallApp(App):

    def build(self):
        return CallInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    app = CallApp()
    app.run()
