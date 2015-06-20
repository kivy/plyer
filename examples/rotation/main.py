'''
Rotation example.
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from plyer import rotation


class RotationTest(BoxLayout):
    def __init__(self):
        super(RotationTest, self).__init__()
        self.sensorEnabled = False

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                rotation.enable()
                Clock.schedule_interval(self.get_readings, 1 / 20.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop rotation"
            else:
                rotation.disable()
                Clock.unschedule(self.get_readings)

                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start rotation"
        except NotImplementedError:
            import traceback

            traceback.print_exc()
            status = "Rotation is not implemented for your platform"
            self.ids.status.text = status

    def get_readings(self, dt):
        val = rotation.rotation

        self.ids.x_label.text = "Azimuth: " + str(val[0])
        self.ids.y_label.text = "Picth: " + str(val[1])
        self.ids.z_label.text = "Roll: " + str(val[2])


class RotationTestApp(App):
    def build(self):
        return RotationTest()


if __name__ == '__main__':
    RotationTestApp().run()
