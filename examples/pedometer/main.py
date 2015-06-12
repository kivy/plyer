from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import pedometer plyer.pedometer
<PedometerInterface>:
    pedometer: pedometer
    orientation: 'vertical'
    padding: '50dp'
    spacing: '20dp'

    BoxLayout:
        orientation: 'horizontal'
        height: None
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
        text: 'Total number of steps:' + str(root.steps)

''')


class PedometerInterface(BoxLayout):
    '''Root Widget.'''

    pedometer = ObjectProperty()
    steps = NumericProperty()

    def enable(self):
        self.pedometer.enable()
        Clock.schedule_interval(self.get_steps, 1 / 20.)

    def disable(self):
        self.pedometer.disable()
        Clock.unschedule(self.get_steps)

    def get_steps(self, dt):
        self.steps = self.pedometer.steps


class PedometerApp(App):

    def build(self):
        return PedometerInterface()

    def on_pause(self):
        return True

if __name__ == "__main__":
    PedometerApp().run()
