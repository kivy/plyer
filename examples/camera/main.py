'''
Basic camera example
Default picture is saved at user_data_dir/test_pic.jpg
This ensures that the path exists
'''
from os.path import exists, join
import kivy
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from plyer import camera
kivy.require('1.9.0')


class CameraDemo(FloatLayout):
    def do_capture(self):
        print()
        filepath = join(App.get_running_app().user_data_dir,
                        self.ids.filename.text)

        if(exists(filepath)):
            popup = MsgPopup(msg="Picture with this name already exists!")
            popup.open()
            return False

        try:
            camera.take_picture(filename=filepath,
                                on_complete=self.camera_callback)
        except NotImplementedError:
            popup = MsgPopup(msg="This feature has not yet been implemented for this platform.")
            popup.open()

    def camera_callback(self, filepath):
        if(exists(filepath)):
            popup = MsgPopup(msg="Picture saved!")
            popup.open()
        else:
            popup = MsgPopup(msg="Could not save your picture!")
            popup.open()


class CameraDemoApp(App):
    def build(self):
        return CameraDemo()

    def on_pause(self):
        return True

    def on_resume(self):
        pass


class MsgPopup(Popup):
    msg = StringProperty()

if __name__ == '__main__':
    CameraDemoApp().run()
