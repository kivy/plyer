import kivy
from kivy.properties import ListProperty

kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from plyer import tts


class Text2SpeechDemo(BoxLayout):
    lang_list = ListProperty()

    def __init__(self, **kwargs):
        super(Text2SpeechDemo, self).__init__(**kwargs)
        self.language = {d['language']: d['voice'] for d in tts.language()}
        self.lang_list = self.language.keys()
        self.ids.lang_select.text = self.lang_list[0]

    def do_read(self):
        try:
            tts.speak(self.ids.speak_text.text,
                      self.language[self.ids.lang_select.text])
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
