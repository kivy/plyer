'''
This example uses Kivy Garden Graph addon to draw graphs plotting the
accelerometer values in X,Y and Z axes.
The package is installed in the directory: ./libs/garden/garden.graph
To read more about kivy garden, visit: http://kivy-garden.github.io/.
'''

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock

from plyer import accelerometer

from kivy.garden.graph import MeshLinePlot

kivy.require('1.8.0')


class AccelerometerDemo(BoxLayout):
    def __init__(self):
        super().__init__()

        self.sensorEnabled = False
        self.graph = self.ids.graph_plot

        # For all X, Y and Z axes
        self.plot = []
        self.plot.append(MeshLinePlot(color=[1, 0, 0, 1]))  # X - Red
        self.plot.append(MeshLinePlot(color=[0, 1, 0, 1]))  # Y - Green
        self.plot.append(MeshLinePlot(color=[0, 0, 1, 1]))  # Z - Blue

        self.reset_plots()

        for plot in self.plot:
            self.graph.add_plot(plot)

    def reset_plots(self):
        for plot in self.plot:
            plot.points = [(0, 0)]

        self.counter = 1

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                accelerometer.enable()
                Clock.schedule_interval(self.get_acceleration, 1 / 20.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop Accelerometer"
            else:
                accelerometer.disable()
                self.reset_plots()
                Clock.unschedule(self.get_acceleration)

                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start Accelerometer"
        except NotImplementedError:
            popup = ErrorPopup()
            popup.open()

    def get_acceleration(self, dt):
        if (self.counter == 100):
            # We re-write our points list if number of values exceed 100.
            # ie. Move each timestamp to the left.
            for plot in self.plot:
                del(plot.points[0])
                plot.points[:] = [(i[0] - 1, i[1]) for i in plot.points[:]]

            self.counter = 99

        val = accelerometer.acceleration[:3]

        if(not val == (None, None, None)):
            self.plot[0].points.append((self.counter, val[0]))
            self.plot[1].points.append((self.counter, val[1]))
            self.plot[2].points.append((self.counter, val[2]))

        self.counter += 1


class AccelerometerDemoApp(App):
    def build(self):
        return AccelerometerDemo()

    def on_pause(self):
        return True


class ErrorPopup(Popup):
    pass


if __name__ == '__main__':
    AccelerometerDemoApp().run()
