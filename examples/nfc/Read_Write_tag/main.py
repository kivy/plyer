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
    ToggleButton:
        text: "Read mode is on" if root.tag_state == "read" else \
              "Write mode is on"
    BoxLayout:
        TextInput:
            id: write_msg
            text: root.write_message
            multiline: True
        Label:
            text: root.read_message

''')


class NFCInterface(BoxLayout):

    tag_state = StringProperty()
    write_msg = StringProperty()
    read_msg = StringProperty()

    def __init__(self, **kwargs):
        super(NFCInterface, self).__init__(**kwargs)
        self.tag_state = self.get_tag_state()

    def alter_state(self):
        if self.tag_state == "read":
            nfc.set_tag_mode(mode='write')
        else:
            nfc_set_tag_mode(mode='read')

    def get_tag_state(self):
        self.tag_state = nfc.get_tag_mode()

    def create_record_for_tag(self):
        return nfc.create_record(ndef_type='application',
                                 payload='org.test.kivy.plyernfcexample')

    def create_message_for_tag(self):
        ndef_record = self.create_record_for_tag()
        self.tag_message = nfc.create_ndef_message_bundle(ndef_record)

    def write_on_tag(self):
        nfc.set_message(self.tag_message)

    def read_tag(self):
        nfc.get_message()

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
