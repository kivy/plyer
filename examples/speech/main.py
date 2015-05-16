from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from plyer import speech


Builder.load_string('''
<SpeechInterface>:
    orientation: 'vertical'
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'Is supported: %s' % root.speech.exist()
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'Results'
    Label:
        id: results
        size_hint_y: 0.7
        height: sp(40)
        text: ''
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'Errors'
    Label:
        id: errors
        size_hint_y: 0.7
        height: sp(40)
        text: ''
    Button:
        id: start_button
        text: 'Start Listening'
        on_release:
            root.start_listening()

''')


class SpeechInterface(BoxLayout):
    '''Root Widget.'''

    speech = speech
    state = StringProperty()

    def start_listening(self):
        start_button = self.ids['start_button']
        start_button.text = 'Stop'

        label_results = self.ids['results']
        label_results.text = ''

        label_errors = self.ids['errors']
        label_errors.text = ''

        self.speech.start()
        self.state = self.speech.state

        Clock.schedule_interval(self.check_state, 1)

    def stop_listening(self):
        start_button = self.ids['start_button']
        start_button.text = 'Start Listening'

        self.speech.stop()
        self.update()

        Clock.unschedule(self.check_state)

    def check_state(self, dt):
        if self.state != self.speech.state:
            self.stop_listening()

    def update(self):
        label_errors = self.ids['errors']
        label_errors.text = '\n'.join(set(self.speech.errors))

        label_results = self.ids['results']
        label_results.text = '\n'.join(set(self.speech.results))

class SpeechApp(App):

    def build(self):
        return SpeechInterface()


    def on_pause(self):
        return True


if __name__ == "__main__":
    SpeechApp().run()
