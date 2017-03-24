from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty


Builder.load_string('''
#:import spellcheck plyer.spellcheck
<SpellCheckInterface>:
    spellcheck: spellcheck
    orientation: 'vertical'
    BoxLayout:
        Label:
            text: 'Input Text'
        TextInput:
            id: inputtext
    Button:
        text: 'Get Suggestions'
        on_press: root.get_suggestions(inputtext.text)
    Label:
        text: root.suggestions
''')


class SpellCheckInterface(BoxLayout):
    '''Root Widget'''

    spellcheck = ObjectProperty()
    suggestions = StringProperty()

    def get_suggestions(self, text):
        self.suggestions = self.spellcheck.get_suggestions(text)


class SpellCheckApp(App):

    def build(self):
        return SpellCheckInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    SpellCheckApp().run()
