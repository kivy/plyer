
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

interface = Builder.load_string('''
#:import facade plyer.orientation
<WrapButton@Button>:
    text_size: self.size
    valign: 'middle'
    halign: 'center'

<OrientationInterface>:
    facade: facade
    orientation: 'vertical'
    padding: '20dp'
    spacing: '10dp'

    BoxLayout:
        orientation: 'horizontal'
        BoxLayout:
            orientation: 'vertical'
            Button:
                id: enable_button
                text: 'Enable Sensor'
                disabled: False
                on_release:
                    root.enable_listener()
                    disable_button.disabled = not disable_button.disabled
                    enable_button.disabled = not enable_button.disabled
            Button:
                id: disable_button
                text: 'Disable Sensor'
                disabled: True
                on_release:
                    root.disable_listener()
                    disable_button.disabled = not disable_button.disabled
                    enable_button.disabled = not enable_button.disabled
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Azimuth: ' + str(root.azimuth)
            Label:
                text: 'Pitch: ' + str(root.pitch)
            Label:
                text: 'Roll: ' + str(root.roll)

    GridLayout:
        cols: 2
        WrapButton:
            text: 'portrait'
            on_release: root.facade.set_portrait()
        WrapButton:
            text: 'portrait reverse'
            on_release: root.facade.set_portrait(reverse=True)
        WrapButton:
            text: 'landscape'
            on_release: root.facade.set_landscape()
        WrapButton:
            text: 'landscape reverse'
            on_release: root.facade.set_landscape(reverse=True)
        WrapButton:
            text: 'free sensor'
            on_release: root.facade.set_sensor(mode='any')
        Widget:
        WrapButton:
            text: 'landscape sensor'
            on_release: root.facade.set_sensor(mode='landscape')
        WrapButton:
            text: 'portrait sensor'
            on_release: root.facade.set_sensor(mode='portrait')
''')


class OrientationInterface(BoxLayout):

    pitch = NumericProperty(0)
    azimuth = NumericProperty(0)
    roll = NumericProperty(0)

    facade = ObjectProperty()

    def enable_listener(self):
        self.facade.enable_listener()
        Clock.schedule_interval(self.get_orientation, 1 / 20.)

    def disable_listener(self):
        self.facade.disable_listener()
        Clock.unschedule(self.get_orientation)

    def get_orientation(self, dt):
        if self.facade.orientation != (None, None, None):
            self.pitch, self.roll, self.azimuth  = self.facade.orientation


class OrientationTestApp(App):
    def build(self):
        return OrientationInterface()

if __name__ == "__main__":
    OrientationTestApp().run()
