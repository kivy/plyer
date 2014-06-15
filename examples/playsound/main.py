'''
Basic PlaySound example
'''

from os import getcwd
from os.path import exists
from os.path import splitext

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger

from plyer import playsound

class PlaySoundDemo(FloatLayout):
    def __init__(self):
        super(PlaySoundDemo, self).__init__()
        soundpath = getcwd() + "/blip.mp3"
        self.ids.path_label.text = soundpath

        playsound.load(soundpath)

    def do_play(self):
        try:
            playsound.play()
        except NotImplementedError:
            popup = MsgPopup(msg="This feature has not yet been implemented for this platform.")
            popup.open()

class PlaySoundDemoApp(App):
    def __init__(self):
        super(PlaySoundDemoApp, self).__init__()
        self.demo = None

    def build(self):
        self.demo = PlaySoundDemo()
        return self.demo

    def on_pause(self):
        return True

    def on_resume(self):
        pass

class MsgPopup(Popup):
    def __init__(self, msg):
        super(MsgPopup, self).__init__()
        self.ids.message_label.text = msg

if __name__ == '__main__':
    PlaySoundDemoApp().run()