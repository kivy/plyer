
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty

from plyer import inappbrowser

Builder.load_string('''
<InAppBrowserInterface>:
    orientation: 'vertical'
    Label:
        id: label
        text: 'Input URL below to go'
    TextInput:
        id: address
        text: 'https://www.github.com'
    IntentButton:
        url_text: address.text
        text: 'Go'
        size_hint_y: None
        height: sp(40)
        on_release: self.go()
''')


class InAppBrowserInterface(BoxLayout):
    pass


class IntentButton(Button):
    url_text = StringProperty()

    def go(self, *args):
        inappbrowser.open_url(url=self.url_text)


class InAppBrowserApp(App):
    def build(self):
        return InAppBrowserInterface()

    def on_pause(self):
        return True

if __name__ == "__main__":
    InAppBrowserApp().run()
