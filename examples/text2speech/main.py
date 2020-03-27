import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from plyer import tts

kivy.require('1.8.0')


class Text2SpeechDemo(BoxLayout):
    def do_read(self):
        try:
            tts.speak(self.ids.notification_text.text)
        except NotImplementedError:
            popup = ErrorPopup()
            popup.open()


class Text2SpeechDemoApp(App):
    def build(self):
        return Text2SpeechDemo()

    def on_pause(self):
        return True


class ErrorPopup(Popup):
    pass


if __name__ == '__main__':
    Text2SpeechDemoApp().run()
