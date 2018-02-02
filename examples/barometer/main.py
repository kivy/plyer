from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import barometer plyer.barometer
<BarometerInterface>:
    barometer: barometer
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
        text: 'Current pressure:' + str(root.pressure) + ' hPa.'

''')


class BarometerInterface(BoxLayout):
    '''Root Widget.'''

    barometer = ObjectProperty()
    pressure = NumericProperty()

    def enable(self):
        self.barometer.enable()
        Clock.schedule_interval(self.get_pressure, 1 / 20.)

    def disable(self):
        self.barometer.disable()
        Clock.unschedule(self.get_pressure)

    def get_pressure(self, dt):
        self.pressure = self.barometer.pressure or self.pressure


class BarometerApp(App):

    def build(self):
        return BarometerInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    BarometerApp().run()
