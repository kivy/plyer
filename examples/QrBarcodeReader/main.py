from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty

from plyer import qrbarcodereader

Builder.load_string('''
<QrBrScnrInterface>:
    orientation: 'vertical'
    Label:
        id: label
        text: 'Barcode Qr Scanner implementation'
    FireButton:
        text: 'start'
        size_hint_y: None
        on_release: self.start()
''')


class QrBrScnrInterface(BoxLayout):
    pass


class FireButton(Button):

    def start(self, *args):
        qrbarcodereader.scan()


class QrBrScnrApp(App):
    def build(self):
        return InAppBrowserInterface()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == "__main__":
    QrBrScnrApp().run()
