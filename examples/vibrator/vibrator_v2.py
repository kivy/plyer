from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import os.path
from os.path import dirname
from kivy.lang import Builder
from kivy.utils import platform

if 'android' == platform:
    # ------------------------------------------- #
    # for permissions
    from android.permissions import Permission, request_permissions, check_permission

    # check permissions
    def check_permissions(perms):
        for perm in perms:
            if check_permission(perm) != True:
                return False
        return True

    # list perms
    perms = [Permission.VIBRATE]
        
    # get perms
    if check_permissions(perms)!= True:
        request_permissions(perms)
    # ------------------------------------------- #

# Builder.load_file('vibrator.kv') # not work
Builder.load_file(os.path.join(dirname(__file__), 'vibrator.kv'))

class VibrationInterface(BoxLayout):
    '''Root Widget.'''
   
    def is_android(self):
        if 'android' == platform:
            return True
        else:
            return False

    def do_nothing(self):
        pass

class VibrationApp(App):
    def build(self):
        return VibrationInterface()

    def on_pause(self):
        return True

if __name__ == "__main__":
    VibrationApp().run()