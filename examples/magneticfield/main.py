from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from plyer import magneticfield


Builder.load_string('''
<MagneticFieldInterface>:
    orientation: 'vertical'

    Label:
        id: x_label
        text: 'X: '

    Label:
        id: y_label
        text: 'Y: '

    Label:
        id: z_label
        text: 'Z: '

    Label:
        id: status
        text: ''

    BoxLayout:
        size_hint_y: None
        height: '48dp'
        padding: '4dp'

        ToggleButton:
            id: toggle_button
            text: 'Start Magnetic Field Sensor'
            on_press: root.do_toggle()

''')

class MagneticFieldInterface(BoxLayout):
    def __init__(self):
        super(MagneticFieldInterface, self).__init__()
        self.sensorEnabled = False

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                magneticfield.enable()
                Clock.schedule_interval(self.get_magnetic, 1 / 20.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop MagneticField Sensor"
            else:
                magneticfield.disable()
                Clock.unschedule(self.get_magnetic)

                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start MagneticField Sensor"
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Magnetic Field sensor is not implemented for your platform"
            self.ids.status.text = status

    def get_magnetic(self, dt):
        val = magneticfield.magnetic[:3]

        if not val == (None, None, None):
            self.ids.x_label.text = "X: " + str(val[0])
            self.ids.y_label.text = "Y: " + str(val[1])
            self.ids.z_label.text = "Z: " + str(val[2])


class MagneticFieldApp(App):
    def build(self):
        return MagneticFieldInterface()


if __name__ == '__main__':
    MagneticFieldApp().run()
