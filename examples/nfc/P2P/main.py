from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty
from plyer import nfc

Builder.load_string('''
<NFCInterface>:
    BoxLayout:
        orientation: ""
        Button:
            text: "Enable NFC"
        Button:
            text: "Disable NFC"

''')


class NFCInterface(BoxLayout):

    def enable_nfc(self):
        nfc.enable()

    def disable_nfc(self):
        nfc.disable()

    def write_tag(self):
        pass

    def read_tag(self):
        pass

    def nfc_enable_ndef_exchange(self):
        nfc.nfc_enable_ndef_exchange()

    def nfc_disable_ndef_exchange(self):
        nfc.nfc_disable_ndef_exchange()


class NFCApp(App):

    def build(self):
        return NFCInterface()

    def on_resume(self):
        nfc.enable()
        return True

    def on_pause(self):
        nfc.disable()
        return True


if __name__ == "__main__":
    app = NFCApp()
    app.run()
