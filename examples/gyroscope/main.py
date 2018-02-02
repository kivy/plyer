from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

interface = Builder.load_string('''
#:import facade plyer.gyroscope
<GyroscopeInterface>:
    facade: facade
    orientation: 'vertical'
    padding: '20dp'
    spacing: '10dp'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .1
            Button:
                id: enable_button
                text: 'Enable Sensor'
                disabled: False
                on_release:
                    root.enable()
                    disable_button.disabled = not disable_button.disabled
                    enable_button.disabled = not enable_button.disabled
            Button:
                id: disable_button
                text: 'Disable Sensor'
                disabled: True
                on_release:
                    root.disable()
                    disable_button.disabled = not disable_button.disabled
                    enable_button.disabled = not enable_button.disabled
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Rate of rotation'
            Label:
                text: 'including drift compensation'
            Label:
                text: '(' + str(root.x_calib) + ','
            Label:
                text: str(root.y_calib) + ','
            Label:
                text: str(root.z_calib) + ')'
            Label:
                text: 'Rate of rotation'
            Label:
                text: 'w/o drift compensation'
            Label:
                text: '(' + str(root.x_speed) + ','
            Label:
                text: str(root.y_speed) + ','
            Label:
                text: str(root.z_speed) + ')'
            Label:
                text: 'Estimated Drift'
            Label:
                text: '(' + str(root.x_drift) + ','
            Label:
                text: str(root.y_drift) + ','
            Label:
                text: str(root.z_drift) + ')'
''')


class GyroscopeInterface(BoxLayout):

    x_calib = NumericProperty(0)
    y_calib = NumericProperty(0)
    z_calib = NumericProperty(0)
    x_speed = NumericProperty(0)
    y_speed = NumericProperty(0)
    z_speed = NumericProperty(0)
    x_drift = NumericProperty(0)
    y_drift = NumericProperty(0)
    z_drift = NumericProperty(0)

    facade = ObjectProperty()

    def enable(self):
        self.facade.enable()
        Clock.schedule_interval(self.get_rotation, 1 / 20.)
        Clock.schedule_interval(self.get_rotation_uncalib, 1 / 20.)

    def disable(self):
        self.facade.disable()
        Clock.unschedule(self.get_rotation)
        Clock.unschedule(self.get_rotation_uncalib)

    def get_rotation(self, dt):
        if self.facade.rotation != (None, None, None):
            self.x_calib, self.y_calib, self.z_calib = self.facade.rotation

    def get_rotation_uncalib(self, dt):
        empty = tuple([None for i in range(6)])

        if self.facade.rotation_uncalib != empty:
            self.x_speed, self.y_speed, self.z_speed, self.x_drift,\
                self.y_drift, self.z_drift = self.facade.rotation_uncalib


class GyroscopeTestApp(App):
    def build(self):
        return GyroscopeInterface()


if __name__ == "__main__":
    GyroscopeTestApp().run()
