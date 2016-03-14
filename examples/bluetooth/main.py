from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from plyer import bluetooth

Builder.load_string('''
<BluetoothInterface>:
    orientation: 'vertical'
    GridLayout:
        cols: 2
        Button:
            text: "Turn on"
            on_press: root.turn_on()
        Button:
            text: "Turn off"
            on_press: root.turn_off()
        Button:
            text: "Visible"
            on_press: root.visible()

''')


class BluetoothInterface(BoxLayout):

    def turn_on(self, *args):
        bluetooth.start()

    def turn_off(self, *args):
        bluetooth.stop()

    def visible(self, *args):
        bluetooth.visible()


class BluetoothApp(App):

    def build(self):
        return BluetoothInterface()

    def on_resume(self):
        bluetooth.on_resume()
        return True

    def on_pause(self):
        bluetooth.on_pause()
        return True

    def on_stop(self):
        bluetooth.on_stop()
        return True

if __name__ == "__main__":
    app = BluetoothApp()
    app.run()
