from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''
#:import bluetooth plyer.bluetooth
<BluetoothInterface>:
    bluetooth: bluetooth
    orientation: 'vertical'
    padding: '50dp'
    spacing: '20dp'
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.3
        Button:
            text: 'Get Bluetooth status'
            on_release:
                root.get_info()
    Label:
        text: str(root.text)
    Label:
        text: str(root.info)
''')


class BluetoothInterface(BoxLayout):
    '''Root Widget.'''

    info = ObjectProperty()
    text = StringProperty()

    text = "Bluetooth: "

    def get_info(self):
        self.info = str(self.bluetooth.info)


class BluetoothApp(App):

    def build(self):
        return BluetoothInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    BluetoothApp().run()
