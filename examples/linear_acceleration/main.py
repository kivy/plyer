from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

interface = Builder.load_string('''
#:import facade plyer.linear_acceleration
<LinearAccelerationInterface>:
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
                text: 'Along_x: ' + str(root.along_x)
            Label:
                text: 'Along_y: ' + str(root.along_y)
            Label:
                text: 'Along_z: ' + str(root.along_z)
''')


class LinearAccelerationInterface(BoxLayout):

    along_x = NumericProperty(0)
    along_y = NumericProperty(0)
    along_z = NumericProperty(0)

    facade = ObjectProperty()

    def enable_listener(self):
        self.facade.enable()
        Clock.schedule_interval(self.get_acceleration, 1 / 20.)

    def disable_listener(self):
        self.facade.disable()
        Clock.unschedule(self.get_acceleration)

    def get_acceleration(self, dt):
        if self.facade.acceleration != (None, None, None):
            self.along_x, self.along_x, self.along_z = self.facade.acceleration


class LinearAccelerationTestApp(App):
    def build(self):
        return LinearAccelerationInterface()

if __name__ == "__main__":
    LinearAccelerationTestApp().run()
