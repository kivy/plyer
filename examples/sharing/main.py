from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from plyer import sharing


Builder.load_string('''
<ShareInterface>:
    orientation: "vertical"
    BoxLayout:
        TextInput:
            id: subject
            text: "Subject"
        TextInput:
            id: message
            text: 'Message'
    Button:
        text: "Share it!"
        on_release: root.share(subject.text, message.text)
    Label:

''')


class ShareInterface(BoxLayout):

    def share(self, extra_subject, extra_text):
        sharing.share_text(extra_subject=extra_subject, extra_text=extra_text)


class ShareApp(App):

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def build(self):
        return ShareInterface()

if __name__ == "__main__":
    app = ShareApp()
    app.run()
