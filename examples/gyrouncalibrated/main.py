from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

interface = Builder.load_string('''
#:import facade plyer.gyrouncalibrated
<GyroUncalibratedInterface>:
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
                text: 'Angular Speed'
            Label:
                text: '(without drift compensation)'
            Label:
                text: 'Along X-axis:'
            Label:
                text: str(root.x_speed) + 'rad/s'
            Label:
                text: 'Along Y-axis:'
            Label:
                text: str(root.y_speed) + 'rad/s'
            Label:
                text: 'Along Z-axis:'
            Label:
                text: str(root.z_speed) + 'rad/s'
            Label:
                text: 'Estimated Drift'
            Label:
                text: 'Along X-axis:'
            Label:
                text: str(root.x_drift) + 'rad/s'
            Label:
                text: 'Along Y-axis:'
            Label:
                text: str(root.y_drift) + 'rad/s'
            Label:
                text: 'Along Z-axis:'
            Label:
                text: str(root.z_drift) + 'rad/s'
''')


class GyroUncalibratedInterface(BoxLayout):

    x_speed = NumericProperty(0)
    y_speed = NumericProperty(0)
    z_speed = NumericProperty(0)
    x_drift = NumericProperty(0)
    y_drift = NumericProperty(0)
    z_drift = NumericProperty(0)

    facade = ObjectProperty()

    def enable_listener(self):
        self.facade.enable_listener()
        Clock.schedule_interval(self.get_rotation, 1 / 20.)

    def disable_listener(self):
        self.facade.disable_listener()
        Clock.unschedule(self.get_rotation)

    def get_rotation(self, dt):
        if self.facade.rotation != (None, None, None, None, None, None):
            self.x_speed, self.y_speed, self.z_speed, self.x_drift,\
                self.y_drift, self.z_drift = self.facade.rotation


class GyroUncalibratedTestApp(App):
    def build(self):
        return GyroUncalibratedInterface()

if __name__ == "__main__":
    GyroUncalibratedTestApp().run()
