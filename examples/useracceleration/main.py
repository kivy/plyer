'''
User Acceleration example.
--------------------------
'''

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from plyer import useracceleration

Builder.load_string('''
<UserAccInterface>:
    orientation: 'vertical'
    spacing: '50dp'

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.3
        Button:
            id: button_enable
            text: 'Enable'
            disbaled: False
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
        id: x_label
        text: 'X: '

    Label:
        id: y_label
        text: 'Y: '

    Label:
        id: z_label
        text: 'Z: '

''')


class UserAccInterface(BoxLayout):
    '''
    Root Widget.
    '''

    def enable(self):
        useracceleration.enable()
        Clock.schedule_interval(self.get_acceleration, 1 / 20.)

    def disable(self):
        useracceleration.disable()
        Clock.unschedule(self.get_acceleration)

    def get_acceleration(self, dt):
        val = useracceleration.acceleration
        self.ids.x_label.text = "X: " + str(val[0])
        self.ids.y_label.text = "Y: " + str(val[1])
        self.ids.z_label.text = "Z: " + str(val[2])


class UserAccTestApp(App):
    def build(self):
        return UserAccInterface()

if __name__ == '__main__':
    UserAccTestApp().run()
