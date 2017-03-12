from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

interface = Builder.load_string('''
#:import facade plyer.geomagneticrotation
<GeomagneticRotationInterface>:
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
                text: 'Along X-axis: ' + str(root.along_x)
            Label:
                text: 'Along Y-axis: ' + str(root.along_y)
            Label:
                text: 'Along Z-axis: ' + str(root.along_z)
''')


class GeomagneticRotationInterface(BoxLayout):

    along_x = NumericProperty(0)
    along_y = NumericProperty(0)
    along_z = NumericProperty(0)

    facade = ObjectProperty()

    def enable_listener(self):
        self.facade.enable_listener()
        Clock.schedule_interval(self.get_vector, 1 / 20.)

    def disable_listener(self):
        self.facade.disable_listener()
        Clock.unschedule(self.get_vector)

    def get_vector(self, dt):
        if self.facade.vector != (None, None, None):
            self.along_x, self.along_y, self.along_z = self.facade.vector


class GeomagneticRotationTestApp(App):
    def build(self):
        return GeomagneticRotationInterface()

if __name__ == "__main__":
    GeomagneticRotationTestApp().run()
