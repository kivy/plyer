
from kivy.base import runTouchApp

from kivy.lang import Builder

interface = Builder.load_string('''
#:import orientation plyer.orientation
BoxLayout:
    orientation: 'horizontal'
    GridLayout:
        size_hint_x: 2
        cols: 2
        Button:
            text: 'portrait'
            on_release: orientation.set_portrait()
        Button:
            text: 'portrait reverse'
            on_release: orientation.set_portrait(reverse=True)
        Button:
            text: 'portrait sensor user'
            on_release: orientation.set_portrait(sensor=True)
        Button:
            text: 'portrait sensor ignore user'
            on_release: orientation.set_portrait(sensor=True, user=False)
        Button:
            text: 'landscape'
            on_release: orientation.set_landscape()
        Button:
            text: 'landscape reverse'
            on_release: orientation.set_landscape(reverse=True)
        Button:
            text: 'landscape sensor user'
            on_release: orientation.set_landscape(sensor=True)
        Button:
            text: 'landscape sensor ignore user'
            on_release: orientation.set_landscape(sensor=True, user=False)
        Button:
            text: 'lock current'
            on_release: orientation.lock()
    Image:
        source: 'data/logo/kivy-icon-512.png'
        allow_stretch: True
        keep_ratio: False
''')

runTouchApp(interface)
