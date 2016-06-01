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
    Label:
        text: "Text Sharing"
    BoxLayout:
        TextInput:
            id: subject
            text: "Subject"
        TextInput:
            id: message
            text: 'Message'
    Button:
        text: "Share Text!"
        on_release: root.share_txt(subject.text, message.text)
    Label:
        text: "Image/s Sharing:"
    Button:
        text: "Share Image"
        on_release: root.share_img(root.images)

''')


class ShareInterface(BoxLayout):

    images = ListProperty(['trees.jpg'])

    def share_txt(self, extra_subject, extra_text):
        sharing.share_text(extra_subject=extra_subject, extra_text=extra_text)

    def share_img(self, images):
        sharing.share_images(images=self.images)


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
