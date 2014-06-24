'''
Compass example.
'''

from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from plyer import compass

class compassTest(BoxLayout):
    def __init__(self):
        super(compassTest, self).__init__()
        self.sensorEnabled = False

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                compass.enable()
                Clock.schedule_interval(self.get_readings, 1 / 20.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop compass"
            else:
                compass.disable()
                Clock.unschedule(self.get_readings)

                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start compass"
        except NotImplementedError:
            import traceback; traceback.print_exc()
            self.ids.status.text = "Compass is not implemented for your platform"

    def get_readings(self, dt):
        val = compass.orientation

        self.ids.x_label.text = "X: " + str(val[0])
        self.ids.y_label.text = "Y: " + str(val[1])
        self.ids.z_label.text = "Z: " + str(val[2])

class compassTestApp(App):
    def build(self):
        return compassTest()

if __name__ == '__main__':
    compassTestApp().run()
