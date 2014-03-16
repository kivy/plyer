
from kivy.base import runTouchApp

from kivy.lang import Builder

interface = Builder.load_string('''
#:import orientation plyer.orientation

<WrapButton@Button>:
    text_size: self.size
    valign: 'middle'
    halign: 'center'

<RedButton@WrapButton>:
    background_color: 1, 0, 0, 1

BoxLayout:
    orientation: 'horizontal'
    GridLayout:
        size_hint_x: 2
        cols: 2
        WrapButton:
            text: 'portrait'
            on_release: orientation.set_portrait()
        WrapButton:
            text: 'portrait reverse'
            on_release: orientation.set_portrait(reverse=True)
        WrapButton:
            text: 'portrait sensor ignore user'
            on_release: orientation.set_portrait(sensor=True, user=False)
        RedButton:
            text: 'portrait sensor user'
            on_release: orientation.set_portrait(sensor=True, user=True)
        WrapButton:
            text: 'landscape'
            on_release: orientation.set_landscape()
        WrapButton:
            text: 'landscape reverse'
            on_release: orientation.set_landscape(reverse=True)
        WrapButton:
            text: 'landscape sensor ignore user'
            on_release: orientation.set_landscape(sensor=True, user=False)
        RedButton:
            text: 'landscape sensor user'
            on_release: orientation.set_landscape(sensor=True, user=True)
        RedButton:
            text: 'lock current'
            on_release: orientation.lock()
        Label:
            text: '(placeholder)'
        WrapButton:
            text: 'free rotate'
            on_release: orientation.set_free(user=False, full=False)
        WrapButton:
            text: 'user limited rotate'
            on_release: orientation.set_free(user=True, full=False)
        WrapButton:
            text: 'full free rotate'
            on_release: orientation.set_free(user=False, full=True)
        RedButton:
            text: 'user limited full rotate'
            on_release: orientation.set_free(user=True, full=True)
            
    BoxLayout:
        orientation: 'vertical'
        Label:
            text_size: self.size
            markup: True
            halign: 'center'
            text: '[color=#ff0000]RED[/color] functions need api level 18 if running on android!'
            size_hint_y: None
            height: sp(80)
        Image:
            source: 'data/logo/kivy-icon-512.png'
            allow_stretch: True
            keep_ratio: False
''')

runTouchApp(interface)
