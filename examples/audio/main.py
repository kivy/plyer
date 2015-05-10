from time import sleep

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

kv = '''
#:import audio androidaudio.audio
BoxLayout:
    orientation: 'vertical'
    padding: '50dp'
    spacing: '20dp'
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'AudioPlayer State: ' + str(audio.state)
    Button:
        text: 'Record' if audio.state == 'stopped' else 'Pause'
        on_release: audio.start() if audio.state == 'stopped' else audio.pause()

    Button:
        text: 'Play'
        #on_release:
        #    vibrator.pattern([float(n) for n in ti.text.split(',')])

    TextInput:
        id: ti
        text: '0.5,0.5,1,2,0.1,0.1,0.1,0.1,0.1,0.1'

'''


class AudioApp(App):

    def build(self):
        return Builder.load_string(kv)

    def on_pause(self):
        return True


if __name__ == "__main__":
    AudioApp().run()


