from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from plyer import sharing
import os
from kivy.uix.filechooser import FileChooserIconView


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
    BoxLayout:
        orientation: "horizontal"
        Button:
            text: "Share Image"
            on_release: root.share_img(root.images)
        Button:
            text: "Multiple File chooser"
            on_press: root.create_popup()
<Content>:
    orientation: "vertical"
    FileChooserIconView:
        id: filechooser
        on_selection: root.selected(filechooser.selection)
    Button:
        size_hint: 1,.2
        text: 'Close!'
        on_release: root.close_chooser()

''')

class Content(BoxLayout):
    def selected(self, filename):
        ShareInterface.selected(filename)
    def close_chooser(self):
        self.parent.parent.parent.dismiss()

class ShareInterface(BoxLayout):

    images = []

    def share_txt(self, extra_subject, extra_text):
        sharing.share_text(extra_subject=extra_subject, extra_text=extra_text)

    def share_img(self, images):
        sharing.share_images(images=self.images)

    @classmethod
    def selected(self, filename):
        self.images.append(filename[0])

    def create_popup(self):
        self.file_chooser = FileChooserIconView()
        self.file_chooser.bind()
        self.popup = Popup(title='File chooser', content=Content(),
                           size_hint=(0.80, 0.80),
                           auto_dismiss=True)
        self.popup.open()


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
