from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import audio_player plyer.audio
<AudioInterface>:
    audio: audio_player
    orientation: 'vertical'
    padding: '50dp'
    spacing: '20dp'
    Label:
        id: state_label
        size_hint_y: None
        height: sp(40)
        text: 'AudioPlayer State: ' + str(root.audio.state)
    Label:
        id: location_label
        size_hint_y: None
        height: sp(40)
        text: 'Recording Location: ' + str(root.audio.file_path)

    Button:
        id: record_button
        text: 'Start Recording'
        on_release: root.start_recording()

    Button:
        id: play_button
        text: 'Play'
        on_release: root.play_recording()

''')


class AudioInterface(BoxLayout):
    '''Root Widget.'''

    audio = ObjectProperty()
    time = NumericProperty(0)

    has_record = False

    def start_recording(self):
        state = self.audio.state
        if state == 'ready':
            self.audio.start()

        if state == 'recording':
            self.audio.stop()
            self.has_record = True

        self.update_labels()

    def play_recording(self):
        state = self.audio.state
        if state == 'playing':
            self.audio.stop()
        else:
            self.audio.play()

        self.update_labels()

    def update_labels(self):
        record_button = self.ids['record_button']
        play_button = self.ids['play_button']
        state_label = self.ids['state_label']

        state = self.audio.state
        state_label.text = 'AudioPlayer State: ' + state

        play_button.disabled = not self.has_record

        if state == 'ready':
            record_button.text = 'Start Recording'

        if state == 'recording':
            record_button.text = 'Press to Stop Recording'
            play_button.disabled = True

        if state == 'playing':
            play_button.text = 'Stop'
            record_button.disabled = True
        else:
            play_button.text = 'Press to play'
            record_button.disabled = False


class AudioApp(App):

    def build(self):
        return AudioInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    AudioApp().run()
