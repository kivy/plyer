
from kivy.base import runTouchApp

from kivy.lang import Builder

interface = Builder.load_string('''
#:import orientation plyer.orientation

<WrapButton@Button>:
    text_size: self.size
    valign: 'middle'
    halign: 'center'

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
            text: 'landscape'
            on_release: orientation.set_landscape()
        WrapButton:
            text: 'landscape reverse'
            on_release: orientation.set_landscape(reverse=True)
        WrapButton:
            text: 'free sensor'
            on_release: orientation.set_sensor(mode='any')
        Widget:
        WrapButton:
            text: 'landscape sensor'
            on_release: orientation.set_sensor(mode='landscape')
        WrapButton:
            text: 'portrait sensor'
            on_release: orientation.set_sensor(mode='portrait')
''')

runTouchApp(interface)
