from kivy.app import App
from kivy.lang import Builder
from plyer import fingerprint
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

Builder.load_string('''
<MsgPopup>:
    size_hint: .7, .4
    title: "Attention"

    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 20

        Label:
            id: message_label
            size_hint_y: 0.4
            text: "Label"
        Button:
            text: 'Dismiss'
            size_hint_y: 0.4
            on_press: root.dismiss()

<FingerprintInterface>:
    orientation: 'vertical'

    BoxLayout:
        orientation: 'vertical'
        Image:
            source: 'icon.png'
        Label:
            text: 'Place your finger over the fingerprint scanner and'
        Label:
            text: 'press the button to authenticate.'
        CheckHardwareButton:
            text: 'Check Hardware'
            on_press: self.check()
        IsFingerprintEnrolledButton:
            text: 'Is Fingerprint Enrolled ?'
            on_press: self.check()
        AuthenticateButton:
            text: 'Authenticate'
            on_press: self.auth()
''')


class FingerprintInterface(BoxLayout):
    pass


class IsFingerprintEnrolledButton(Button):

    def check(self):
        try:
            if fingerprint.is_enrolled():
                popup = MsgPopup(
                    "At least one fingerprint is enrolled.")
                popup.open()
            else:
                popup = MsgPopup(
                    "No fingerprint is enrolled.")
                popup.open()
        except NotImplementedError:
            popup = MsgPopup(
                "This feature has not yet been implemented for this platform.")
            popup.open()


class CheckHardwareButton(Button):

    def check(self):
        try:
            if fingerprint.check_hardware():
                popup = MsgPopup(
                    "Fingerprint Scanner present.")
                popup.open()
            else:
                popup = MsgPopup(
                    "Fingerprint Scanner not present.")
                popup.open()
        except NotImplementedError:
            popup = MsgPopup(
                "This feature has not yet been implemented for this platform.")
            popup.open()


class AuthenticateButton(ToggleButton):

    def auth(self):
        try:
            if fingerprint.authenticate():
                popup = MsgPopup(
                    "Fingerprint Authentication Succeeded.")
                popup.open()
            else:
                popup = MsgPopup(
                    "FIngerprit Authentication Failed.")
                popup.open()
        except NotImplementedError:
            popup = MsgPopup(
                "This feature has not yet been implemented for this platform.")
            popup.open()


class MsgPopup(Popup):
    def __init__(self, msg):
        super(MsgPopup, self).__init__()
        self.ids.message_label.text = msg


class FingerprintApp(App):

    def build(self):
        return FingerprintInterface()


if __name__ == '__main__':
    FingerprintApp().run()
