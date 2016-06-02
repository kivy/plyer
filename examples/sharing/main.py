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
            on_press: root.create_img_popup()
    Label:
        text: "File/s Sharing"
    BoxLayout:
        orientation: "horizontal"
        Button:
            text: "Share Files"
            on_release: root.share_fls(root.files)
        Button:
            text: "Multiple File chooser"
            on_press: root.create_fls_popup()

<Content_img>:
    orientation: "vertical"
    FileChooserIconView:
        id: filechooser_img
        on_selection: root.selected_img(filechooser_img.selection)
    Button:
        size_hint: 1,.2
        text: 'Close!'
        on_release: root.close_chooser()

<Content_fls>:
    orientation: "vertical"
    FileChooserIconView:
        id: filechooser_fls
        on_selection: root.selected_fls(filechooser_fls.selection)
    Button:
        size_hint: 1,.2
        text: 'Close!'
        on_release: root.close_chooser()

''')


class Content_img(BoxLayout):

    def selected_img(self, filename):
        ShareInterface.selected_img(filename)

    def close_chooser(self):
        self.parent.parent.parent.dismiss()


class Content_fls(BoxLayout):

    def selected_fls(self, filename):
        ShareInterface.selected_fls(filename)

    def close_chooser(self):
        self.parent.parent.parent.dismiss()


class ShareInterface(BoxLayout):

    images = []
    files = []

    def share_txt(self, extra_subject, extra_text):
        sharing.share_text(extra_subject=extra_subject, extra_text=extra_text)

    def share_img(self, images):
        sharing.share_images(images=self.images)

    def share_fls(self, files):
        sharing.share_files(files=files)

    @classmethod
    def selected_img(self, filename):
        self.images.append(filename[0])

    @classmethod
    def selected_fls(self, filename):
        self.files.append(filename[0])

    def create_img_popup(self):
        self.popup = Popup(title='Image/s chooser', content=Content_img(),
                           size_hint=(0.80, 0.80),
                           auto_dismiss=True)
        self.popup.open()

    def create_fls_popup(self):
        self.popup = Popup(title='Files chooser', content=Content_fls(),
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
