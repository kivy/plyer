from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import facade plyer.humidity
<HumidityInterface>:
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
        text: 'Humidity: ' + str(root.humidity)
''')


class HumidityInterface(BoxLayout):
    '''Root Widget.'''
    humidity = NumericProperty(0)
    facade = ObjectProperty()

    def enable(self):
        self.facade.enable()
        Clock.schedule_interval(self.tell, 1 / 20.)

    def disable(self):
        self.facade.disable()
        Clock.unschedule(self.tell)

    def tell(self, dt):
        if self.facade.tell is not None:
            self.humidity = self.facade.tell


class HumidityApp(App):

    def build(self):
        return HumidityInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    HumidityApp().run()
