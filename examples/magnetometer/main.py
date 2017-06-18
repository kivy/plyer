from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import facade plyer.magnetometer
<MagnetometerInterface>:
    facade: facade
    orientation: 'vertical'
    padding: '50dp'
    spacing: '20dp'
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.3
        Button:
            id: button_enable
            text: 'Enable'
            disabled: False
            on_release:
                root.enable()
                button_disable.disabled = not button_disable.disabled
                button_enable.disabled = not button_enable.disabled
        Button:
            id: button_disable
            text: 'Disable'
            disabled: True
            on_release:
                root.disable()
                button_disable.disabled = not button_disable.disabled
                button_enable.disabled = not button_enable.disabled
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Along_x: ' + str(root.along_x)
        Label:
            text: 'Along_y: ' + str(root.along_y)
        Label:
            text: 'Along_z: ' + str(root.along_z)
''')


class MagnetometerInterface(BoxLayout):
    '''Root Widget.'''
    along_x = NumericProperty(0)
    along_y = NumericProperty(0)
    along_z = NumericProperty(0)
    facade = ObjectProperty()

    def enable(self):
        self.facade.enable()
        Clock.schedule_interval(self.get_field, 1 / 20.)

    def disable(self):
        self.facade.disable()
        Clock.unschedule(self.get_field)

    def get_field(self, dt):
        if self.facade.field != (None, None, None):
            self.along_x, self.along_y, self.along_z = self.facade.field


class MagnetometerApp(App):
    def build(self):
        return MagnetometerInterface()

    def on_pause(self):
        return True

if __name__ == "__main__":
    MagnetometerApp().run()
