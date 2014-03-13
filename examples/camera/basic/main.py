'''
Basic camera example
Default picture is saved as /sdcard/org.test.cameraexample/enter_file_name_here.jpg
'''

import os

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from plyer import camera

class CameraDemo(FloatLayout):
    def __init__(self):
        super(CameraDemo, self).__init__()
        self.cwd = os.getcwd() + "/"            
        self.ids.path_label.text = self.cwd

    def do_capture(self):
        try:
        
            filepath = self.cwd + self.ids.filename_text.text
            camera.take_picture(filename=filepath, 
                                on_complete=self.camera_callback)
        except NotImplementedError:
            popup = MsgPopup(msg="This feature has not yet been implemented for this platform.")
            popup.open()

    def camera_callback(self, **kwargs):
        return False

class CameraDemoApp(App):
    def build(self):
        return CameraDemo()

class MsgPopup(Popup):
    def __init__(self, msg):
        super(MsgPopup, self).__init__()

        self.ids.message_label.text = msg

if __name__ == '__main__':
    CameraDemoApp().run()
    