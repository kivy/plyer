from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

interface = Builder.load_string('''
#:import facade plyer.spatialorientation

<SpOrientationInterface>:
    facade: facade
    orientation: 'vertical'
    padding: '20dp'
    spacing: '10dp'

    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
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
                text: 'Azimuth: ' + str(root.azimuth) + ' radians'
            Label:
                text: 'Pitch: ' + str(root.pitch) + ' radians'
            Label:
                text: 'Roll: ' + str(root.roll) + ' radians'

''')


class SpOrientationInterface(BoxLayout):

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
            self.azimuth, self.pitch, self.roll = self.facade.orientation


class SpOrientationTestApp(App):
    def build(self):
        return SpOrientationInterface()


if __name__ == "__main__":
    SpOrientationTestApp().run()
