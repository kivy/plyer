from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from plyer import speech

Builder.load_string('''
#:import speech plyer.speech

<SpeechInterface>:
    orientation: 'vertical'
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'Is supported: %s' % speech.exist()
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'Possible Matches'
    TextInput:
        id: results
        hint_text: 'results (auto stop)'
        size_hint_y: 0.3
    TextInput:
        id: partial
        hint_text: 'partial results (manual stop)'
        size_hint_y: 0.3
    TextInput:
        id: errors
        size_hint_y: None
        height: sp(20)
    Button:
        id: start_button
        text: 'Start Listening'
        on_release:
            root.start_listening()

''')


class SpeechInterface(BoxLayout):
    '''Root Widget.'''

    def start_listening(self):
        if speech.listening:
            self.stop_listening()
            return

        start_button = self.ids.start_button
        start_button.text = 'Stop'

        self.ids.results.text = ''
        self.ids.partial.text = ''

        speech.start()

        Clock.schedule_interval(self.check_state, 1 / 5)

    def stop_listening(self):
        start_button = self.ids.start_button
        start_button.text = 'Start Listening'

        speech.stop()
        self.update()

        Clock.unschedule(self.check_state)

    def check_state(self, dt):
        # if the recognizer service stops, change UI
        if not speech.listening:
            self.stop_listening()

    def update(self):
        self.ids.partial.text = '\n'.join(speech.partial_results)
        self.ids.results.text = '\n'.join(speech.results)


class SpeechApp(App):

    def build(self):
        return SpeechInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    SpeechApp().run()
