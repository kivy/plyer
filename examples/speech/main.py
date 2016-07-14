from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from plyer import stt
from kivy.lang import Builder
Builder.load_string('''
<STTDemo>:
    Button:
        text: "Start listening"
        on_release: root.start()
    Button:
        text: "Stop listening"
        on_release: root.stop()

    Button:
        text: "Set Commands"
        on_release: root.set_command()

    Button:
        text: "commands title"
        on_release: root.commands_title()

    Button:
        text: "commands"
        on_release: root.commands()

''')


class STTDemo(BoxLayout):

    def start(self):
        stt.start_listening()

    def stop(self):
        stt.stop_listening()

    def set_command(self):
        stt.set_commands()

    def commands_title(self):
        print stt.display_commands_title()

    def commands(self):
        print stt.display_commnds()


class SpeechToTextApp(App):
    def build(self):
        return STTDemo()

if __name__ == '__main__':
    SpeechToTextApp().run()
