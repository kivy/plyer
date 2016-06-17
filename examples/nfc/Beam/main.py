from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from plyer import nfc
import os
from kivy.uix.filechooser import FileChooserIconView


Builder.load_string('''
<BeamInterface>:
    orientation: "vertical"
    Label:
        size_hint: 1, .5
        text: "Beaming Files :D"
    GridLayout:
        cols: 2
        padding: 20
        spacing: 20
        Label:
            text: "Step 1:"
        BoxLayout:
            orientation: "vertical"
            spacing: 20
            Button:
                text: "Milti-Files chooser"
                on_release: root.create_fls_popup()
            Button:
                text: "clear list!"
                on_release: root.clear_list()
        Label:
            text: "Step 2"
        Button:
            text: "Beam it!"
            on_release: root.beam_it(root.files)

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


class Content_fls(BoxLayout):

    def selected_fls(self, filename):
        BeamInterface.selected_fls(filename)

    def close_chooser(self):
        self.parent.parent.parent.dismiss()


class BeamInterface(BoxLayout):

    files = []

    def beam_it(self, files):
        # print files
        nfc.nfc_beam(files=files)

    @classmethod
    def clear_list(self):
        self.files = []

    @classmethod
    def selected_fls(self, filename):
        self.files.append(filename[0])

    def create_fls_popup(self):
        self.popup = Popup(title='Files chooser', content=Content_fls(),
                           size_hint=(0.80, 0.80),
                           auto_dismiss=True)
        self.popup.open()


class BeamApp(App):

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def build(self):
        return BeamInterface()

if __name__ == "__main__":
    app = BeamApp()
    app.run()
