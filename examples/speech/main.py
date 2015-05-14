from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from android_speech_recognition import instance

speech = instance()

Builder.load_string('''
<SpeechInterface>:
    orientation: 'vertical'
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'vibrator exists: '
    TextInput:
        id: ti
        text: '0.5,0.5,1,2,0.1,0.1,0.1,0.1,0.1,0.1'
    Button:
        text: 'vibrate pattern'
        on_release:
            root.start_listening()

''')


class SpeechInterface(BoxLayout):
    '''Root Widget.'''
    def start_listening(self):
        speech.start()


class SpeechApp(App):

    def build(self):
        return SpeechInterface()


    def on_pause(self):
        return True


if __name__ == "__main__":
    SpeechApp().run()
