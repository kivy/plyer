from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import temperature plyer.temperature
<TemperatureInterface>:
    temperature: temperature
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
    Label:
        text: 'Current air temperature: ' + str(root.temp) + ' degrees C.'
''')


class TemperatureInterface(BoxLayout):
    '''Root Widget.'''

    temperature = ObjectProperty()
    temp = NumericProperty()

    def enable(self):
        self.temperature.enable()
        Clock.schedule_interval(self.get_temperature, 1 / 20.)

    def disable(self):
        self.temperature.disable()
        Clock.unschedule(self.get_temperature)

    def get_temperature(self, dt):
        self.temp = self.temperature.temperature or self.temp


class TemperatureApp(App):

    def build(self):
        return TemperatureInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    TemperatureApp().run()
