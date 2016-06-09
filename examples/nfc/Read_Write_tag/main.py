from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from plyer import nfc

Builder.load_string('''
<NFCInterface>:
    BoxLayout:
        Button:
            text: "Enable NFC"
            on_release: root.enable_nfc()
        Button:
            text: "Disable NFC"
            on_release: root.disable_nfc()
    BoxLayout:
        Button:
            text: "Write to tag"
            on_release: root.write_tag()
        TextInput:
            id: write_msg
            text: "Message Here"
            multiline: True
    Label:
        id: root.read_msg
        text: "Message from tag"

''')


class NFCInterface(BoxLayout):

    write_msg = StringProperty()
    read_msg = StringProperty()

    def enable_nfc(self):
        nfc.enable()

    def disable_nfc(self):
        nfc.disable()

    def write_tag(self):
        nfc.write_tag

    def read_tag(self):
        self.read_msg = str(nfc.tag_message)

    def nfc_enable_ndef_exchange(self):
        nfc.nfc_enable_ndef_exchange()

    def nfc_disable_ndef_exchange(self):
        nfc.nfc_disable_ndef_exchange()


class NFCApp(App):

    def build(self):
        nfc.nfc_init()
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
