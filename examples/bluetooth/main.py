from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty
from plyer import bluetooth

Builder.load_string('''
<BluetoothInterface>:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        Button:
            text: "Turn on"
            on_press: root.turn_on()
        Button:
            text: "Turn off"
            on_press: root.turn_off()
        Button:
            text: "Visible"
            on_press: root.visible()
        Button:
            text: "Discovery"
            on_press: root.discovery()
        Button:
            text: str(root.is_enabled)
            on_press: root.is_enbl()

    BoxLayout:
        Button:
            text: "Paired devices"
            on_press: root.paired_dev()
        Label:
            text: str(root.paired)
    BoxLayout:
        Button:
            text: "Scanned Devices"
            on_press: root.scanned_dev()
        Label:
            text: str(root.scanned)


''')


class BluetoothInterface(BoxLayout):
    paired = ListProperty()
    scanned = ListProperty()
    is_enabled = BooleanProperty(False)

    def turn_on(self, *args):
        bluetooth.enable()

    def turn_off(self, *args):
        bluetooth.disable()

    def visible(self, *args):
        bluetooth.visible()

    def paired_dev(self, *args):
        self.paired = bluetooth.get_paired_devices()

    def scanned_dev(self, *args):
        self.scanned = bluetooth.get_scan_devices()

    def discovery(self, *args):
        bluetooth.start_discovery()

    def is_enbl(self, *args):
        self.is_enabled = bluetooth.is_enabled()


class BluetoothApp(App):

    def build(self):
        return BluetoothInterface()

    def on_resume(self):
        return True

    def on_pause(self):
        return True

    def on_stop(self):
        bluetooth.on_stop()
        return True

if __name__ == "__main__":
    app = BluetoothApp()
    app.run()
