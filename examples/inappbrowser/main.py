from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from plyer import inappbrowser

Builder.load_string('''
<InAppBrowserInterface>:
    orientation: 'vertical'
    Label:
        id: url_label
        text: 'Please input URL to start'
    TextInput:
        id: entered_url
        text: 'https://kivy.org/#home'
    URLfireButton:
        url_input: entered_url.text
        text: 'Enter'
        size_hint_y: None
        on_release: self.openurl()
''')


class InAppBrowserInterface(BoxLayout):
    pass


class URLfireButton(Button):
    url_input = StringProperty()

    def openurl(self, *args):
        inappbrowser.open_url(url=self.url_input)


class InAppBrowserSampleApp(App):

    def build(self):
        return InAppBrowserInterface()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == "__main__":
    InAppBrowserSampleApp().run()
