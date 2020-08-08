from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import proximity plyer.proximity
<ProximityInterface>:
    proximity: proximity
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
        text: 'Does Proximity Sensor detect something?'
    Label:
        text: 'Yes' if root.is_near else 'No'

    Widget:
    Label:
        text: 'Cover with your hand'
    Label:
        text: 'a top part of phone to see result.'
''')


class ProximityInterface(BoxLayout):
    '''Root Widget.'''

    proximity = ObjectProperty()
    is_near = BooleanProperty(False)

    def enable(self):
        self.proximity.enable()
        Clock.schedule_interval(self.get_proxime, 1 / 20.)

    def disable(self):
        self.proximity.disable()
        Clock.unschedule(self.get_proxime)

    def get_proxime(self, dt):
        self.is_near = self.proximity.proximity


class ProximityApp(App):

    def build(self):
        return ProximityInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    ProximityApp().run()
