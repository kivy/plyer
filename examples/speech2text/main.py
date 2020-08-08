from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from plyer import stt

Builder.load_string('''
#:import stt plyer.stt

<SpeechInterface>:
    orientation: 'vertical'
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'Is supported: %s' % stt.exist()
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'Possible Matches'
    TextInput:
        id: results
        hint_text: 'results (auto stop)'
    TextInput:
        id: partial
        hint_text: 'partial results (manual stop)'
    TextInput:
        id: errors
        hint_text: 'errors'
    Button:
        id: start_button
        text: 'Start Listening'
        on_release: root.start_listening()
''')


class SpeechInterface(BoxLayout):
    '''Root Widget.'''

    def start_listening(self):
        if stt.listening:
            self.stop_listening()
            return

        start_button = self.ids.start_button
        start_button.text = 'Stop'

        self.ids.results.text = ''
        self.ids.partial.text = ''

        stt.start()

        Clock.schedule_interval(self.check_state, 1 / 5)

    def stop_listening(self):
        start_button = self.ids.start_button
        start_button.text = 'Start Listening'

        stt.stop()
        self.update()

        Clock.unschedule(self.check_state)

    def check_state(self, dt):
        # if the recognizer service stops, change UI
        if not stt.listening:
            self.stop_listening()

    def update(self):
        self.ids.partial.text = '\n'.join(stt.partial_results)
        self.ids.results.text = '\n'.join(stt.results)


class SpeechApp(App):

    def build(self):
        return SpeechInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    SpeechApp().run()
