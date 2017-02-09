from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from plyer import nfc

Builder.load_string('''
<NFCInterface>:
    orientation: "vertical"
    BoxLayout:
        Button:
            text: "Enable NFC"
            on_release: root.enable_nfc()
        Button:
            text: "Disable NFC"
            on_release: root.disable_nfc()
        Button:
            text: "Enable Ndef Push"
            on_release: root.enable_ndef_push()
        Button:
            text: "Disable Ndef Push"
            on_release: root.disable_ndef_push()
''')


class NFCInterface(BoxLayout):

    def create_record(self):
        return nfc.create_record(ndef_type='mime',
                                 payload={mime_type: 'text/plain',
                                          mime_data: 'Hello World!'})

    def create_message_for_tag(self):
        ndef_record = self.create_record_for_tag()
        self.tag_message = nfc.create_ndef_message_bundle(ndef_record)

    def enable_ndef_push(self):
        nfc.enable_foreground_ndef_push()

    def disable_ndef_push(self):
        nfc.disable_foreground_ndef_push()

    def enable_nfc(self):
        nfc.enable()

    def disable_nfc(self):
        nfc.disable()


class NFCApp(App):

    def build(self):
        nfc.nfc_register(tech_list={'all'},
                         action_list={'ndef', 'tech', 'tag'},
                         data_type="*/*")
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
