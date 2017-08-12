from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import facade plyer.gyroscope
<GyroscopeInterface>:
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

    Label:
        text: 'Along_x:' + str(root.along_x) + ' rad/s'
    Label:
        text: 'Along_y:' + str(root.along_y) + ' rad/s'
    Label:
        text: 'Along_z:' + str(root.along_z) + ' rad/s'

''')


class GyroscopeInterface(BoxLayout):
    '''Root Widget.'''

    facade = ObjectProperty()
    along_x = NumericProperty()
    along_y = NumericProperty()
    along_z = NumericProperty()

    def enable(self):
        self.facade.enable()
        Clock.schedule_interval(self.get_orientation, 1 / 20.)

    def disable(self):
        self.facade.disable()
        Clock.unschedule(self.get_orientation)

    def get_orientation(self, dt):
        if self.facade.orientation != (None, None, None):
            self.along_x, self.along_y, self.along_z = self.facade.orientation


class GyroscopeApp(App):

    def build(self):
        return GyroscopeInterface()

    def on_pause(self):
        return True

if __name__ == "__main__":
    GyroscopeApp().run()
