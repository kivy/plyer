"""
Basic camera example
Default picture is saved as
/sdcard/org.test.cameraexample/enter_file_name_here.jpg
"""

from os import getcwd
from os.path import exists

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import kivy

from plyer import camera

kivy.require('1.8.0')


class CameraDemo(FloatLayout):
    def __init__(self):
        super().__init__()
        self.cwd = getcwd() + "/"
        self.ids.path_label.text = self.cwd

    def do_capture(self):
        filepath = self.cwd + self.ids.filename_text.text

        if(exists(filepath)):
            popup = MsgPopup("Picture with this name already exists!")
            popup.open()
            return False

        try:
            camera.take_picture(filename=filepath,
                                on_complete=self.camera_callback)
        except NotImplementedError:
            popup = MsgPopup(
                "This feature has not yet been implemented for this platform.")
            popup.open()

    def camera_callback(self, filepath):
        if(exists(filepath)):
            popup = MsgPopup("Picture saved!")
            popup.open()
        else:
            popup = MsgPopup("Could not save your picture!")
            popup.open()


class CameraDemoApp(App):
    def __init__(self):
        super().__init__()
        self.demo = None

    def build(self):
        self.demo = CameraDemo()
        return self.demo

    def on_pause(self):
        return True

    def on_resume(self):
        pass


class MsgPopup(Popup):
    def __init__(self, msg):
        super().__init__()
        self.ids.message_label.text = msg


if __name__ == '__main__':
    CameraDemoApp().run()
