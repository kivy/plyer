from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
from plyer import smsreceive

Builder.load_string('''
<ReceiveSmsInterface>:
    orientation: 'vertical'
    Label:
        text: 'Receive SMS Interface'

    BroadcastButton:
        text: "Press to start service"
        on_press: self.start()

''')


class ReceiveSmsInterface(BoxLayout):
    pass


class BroadcastButton(ToggleButton):
    def start(self):
        smsreceive.startreceiver()


class ReceiveSmsApp(App):
    def build(self):
        return ReceiveSmsInterface()

    def on_pause(self):
        return True

if __name__ == '__main__':
    ReceiveSmsApp().run()
