import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from plyer import tts

class Text2SpeechDemo(BoxLayout):
    def do_read(self):
        tts.speak(self.ids.notification_text.text)

class Text2SpeechDemoApp(App):
    def build(self):
        return Text2SpeechDemo()

if __name__ == '__main__':
    Text2SpeechDemoApp().run()

