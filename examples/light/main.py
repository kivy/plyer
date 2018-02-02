from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import light plyer.light
<LightInterface>:
    light: light
    orientation: 'vertical'
    padding: '50dp'
    spacing: '50dp'

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
        text: 'Current illumination:' + str(root.illumination) + ' lx.'


''')


class LightInterface(BoxLayout):
    '''Root Widget.'''

    light = ObjectProperty()
    illumination = NumericProperty()

    def enable(self):
        self.light.enable()
        Clock.schedule_interval(self.get_illumination, 1 / 20.)

    def disable(self):
        self.light.disable()
        Clock.unschedule(self.get_illumination)

    def get_illumination(self, dt):
        self.illumination = self.light.illumination or self.illumination


class LightApp(App):

    def build(self):
        return LightInterface()

    def on_pause(self):
        return True


if __name__ == '__main__':
    LightApp().run()
